#/usr/bin/env python
import inspect

class Gato():
    
    def __init__(self, function, nargs=None, needs_the_rest=None):
        """
        Try and use inspect to figure out how many args to pop
        off of the stack, and flag whether the function takes 
        variable arguments. In some cases (e.g. when dealing with
        functions implemented in C), inspect can't get this for us,
        so provide the option to specify this manually.
        """
        self._function = function
        if nargs == None and needs_the_rest == None:
            argspec = inspect.getargspec(function)
            self._nargs = len(argspec.args)
            self._needs_the_rest = bool(argspec.varargs)
        else:
            self._nargs = nargs
            self._needs_the_rest = bool(needs_the_rest)
        
    def __repr__(self):
        return self._function.func_name

    def __add__(self, liszt):
        """
        Use the + operator in the middle of a chain of gatos
        to easily put arbitrary values on the stack.
        """
        return gato_compose(self, _put(*liszt))
            
    def __call__(self, *args, **kwargs):
        """
        Call Gato-annotated functions just like normal ones!
        """
        return self._function(*args, **kwargs)
    
    def partial(self, *args, **kwargs):
        """
        Partially apply a Gato.
        """
        if kwargs:
            return gato_compose(gato_compose(_put(*list(args)),_put(kwargs)), self)
        else:
            return gato_compose(_put(*list(args)), self)
    
    def __ror__(self, stack):
        """
        Overload the | operator, but from the right side, which makes
        it workable within python's left-to-right interpretation.

        Credit for figuring out this use of __ror__ lies entirely with
        Julien Palard , whose iterator-oriented Pipe library^ very
        heavily inspired this.
        
        ^see https://github.com/JulienPalard/Pipe
        """
        if isinstance(stack, Gato):
            #if a Gato is the first thing we have, interpret this as composition
            return gato_compose(stack, self)
        if isinstance(stack[-1], dict):
            #use a dict in the top spot as kwargs
            kwargs = stack.pop()
            if self._needs_the_rest:
                return self._function(*stack[-2::-1], **kwargs)
            else:
                incoming = _multipop(stack, self._nargs-len(kwargs))
                return stack + _restack(self._function(*incoming, **kwargs))
        if self._needs_the_rest:
            #is our internal function *arged? then give it the whole stack
            return self._function(*stack[::-1])
        else:
            #else, give it however many it needs
            incoming = _multipop(stack, self._nargs)
            return stack + _restack(self._function(*incoming))

def gato_compose(a, b):
    return Gato(lambda *x: list(reversed(x)) | a | b)

def catmap(starting_stack, *functions):
    """
    If you don't want a permanent Gato version of your fns 
    lying around, this is easier than:
    starting_stack | Gato(function0) | Gato(function1) | Gato(function2)...

    You can also use it like a cheap imitation of clojure's -> operator:

    catmap([1],
           lambda x: x+1,
           lambda x: x*2)
    >> 4
    """
    return reduce(lambda left, right: right.__ror__(left), 
                  map(_gatify, functions),
                  starting_stack)

def _restack(function_return_values):
    return list(reversed(_listify(function_return_values)))

def _gatify(source):
    if isinstance(source, Gato):
        return source
    else:
        return Gato(source)

def _listify(*args):
    if len(args)==0:
        return []
    elif len(args)==1:
        if type(args[0]) is list:
            return list(reversed(args[0]))
        if type(args[0]) is tuple:
            return list(args[0])
        return [args[0]]
    else:
        return list(args)

def _multipop(liszt, n): #MUTATES LISZT
    ret = []
    while n > 0:
        ret.append(liszt.pop())
        n -= 1
    return ret

_put = lambda *x: Gato(lambda: list(x))

##Some basic Gatos, to get you started

#swap the top two items
swap = Gato(lambda x,y: (y,x))

#duplicate the top item
dup = Gato(lambda x: (x,x))

#multiply the top two items, and put result on the stack
mult = Gato(lambda x,y: x*y)

div = Gato(lambda x,y: x/y)

#square the top item - hey look, composition!
square = dup | mult

#add the top two items, and put result on the stack
add = Gato(lambda x, y: x+y)

#remove top item from the stack
rem = Gato(lambda x: ())

#bunch the stack up into one list item
bunch = Gato(lambda *x: [list(reversed(x))])

#repeat the penultimate item (ultimate item) times
rep = Gato(lambda x,y: tuple([y]*x))

#filter the stack based on some predicate function
#
#[4,5] == [1,2,3,4,5] | where(lambda x: x>3)
where = lambda pred: bunch | Gato(filter, 2).partial(pred)

#print the state of the stack and return
@Gato
def tee(*x):
    print x
    return x
