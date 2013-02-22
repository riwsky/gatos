import inspect

def multipop(liszt, n):
    ret = []
    while n > 0:
        ret.append(liszt.pop())
        n -= 1
    return ret

def gatocompose(a, b):
    return Gato(lambda *x: list(reversed(x)) | a | b)

class Gato():
    
    def __init__(self, function, nargs=None, needs_the_rest=None):
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
            
    def __call__(self, *args, **kwargs):
        return self._function(*args, **kwargs)
    
    def partial(self, *args, **kwargs):
        if kwargs:
            return gatocompose(gatocompose(put(*list(args)),put(kwargs)), self)
        else:
            return gatocompose(put(*list(args)), self)
    
    def __ror__(self, stack):
        if isinstance(stack, Gato):
            return gatocompose(stack, self)
        if isinstance(stack[-1], dict):
            kwargs = stack.pop()
            if self._needs_the_rest:
                return self._function(*stack[-2::-1], **kwargs)
            else:
                incoming = multipop(stack, self._nargs-len(kwargs))
                return stack + restack(self._function(*incoming, **kwargs))
        if self._needs_the_rest:
            return self._function(*stack[::-1])
        else:
            incoming = multipop(stack, self._nargs)
            return stack + restack(self._function(*incoming))

def listify(*args):
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

def restack(function_return_values):
    return list(reversed(listify(function_return_values)))


swap = Gato(lambda x,y: (y,x))
dup = Gato(lambda x: (x,x))
mult = Gato(lambda x,y: x*y)
add = Gato(lambda x, y: x+y)
bunch = Gato(lambda *x: [list(reversed(x))])
where = lambda pred: bunch | Gato(filter, 2).partial(pred)
swap = Gato(lambda v, y: (y,v))
dup = Gato(lambda x: (x,x))
put = lambda *x: Gato(lambda: list(x))

grab = lambda *x: sum(x[:1])

def gatify(source):
    if isinstance(source, Gato):
        return source
    else:
        return Gato(source)

def catmap(startpoint, *functions):
    return reduce(lambda left, right: right.__ror__(left), map(Gato, functions), startpoint)

@Gato
def tee(*x):
    print x
    return x

[4,3,2,1] | Gato(lambda x, y: x*y) | swap | dup | put(5,3,4)

