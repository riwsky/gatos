#Gatos 
conCATenative functions for Python.

Ever find yourself writing code that looks like this:

	return reduce(lambda x,y: x+y, 
		filter(in_current_promotion_area, 
			map(calculate_profit_potential, 
				find_spending_history(*users))))
			   			   					
?

Python makes it easy to write functional, composable code—but it doesn’t always make it pretty. That’s where gatos come in:
	
	return users | find_spending_history \
				 | transform(calculate_profit_potential) \
		   		 | where(in_current_promotion_area) \
		   		 | aggregate(sum)

Gatos (Spanish for “cats”) are functions that start with a list, and pop and push elements from/to it as they go along—the concatenative behavior that gives them their name. 

##Usage

So, how does one have to contort their functions’ innards to make them take arguments like this?

Not at all:

	@Gato
	def dup(x):
		return x,x
		
	>>> [1,2,3] | dup
	[1, 2, 3, 3]
	
	mult = Gato(lambda x,y: x*y)
			
	>>>[1,2,3] | mult
	[1,6]
	
Gatos use [inspect](http://docs.python.org/2/library/inspect.html) to figure out how many items a function needs from the stack, passing the stack as a whole to functions which use *args. If desired, you can override these argument number suggestions with your own. 

Gatos still work as normal functions:
	
	>>> dup(3)
	(3, 3)
	
...can be partially applied:

	>>>[1,2,3] : mult.partial(4)
	[1,2,12]

... and can even be composed! Just don’t give them a starting stack:

	square = dup | mult
	
	>>>[1,2,3] | square
	[1,2,9]
	
	>>>square(3)
	[9]
	
This can make higher-level programming look prettier without restricting implementation details. Along with some syntactic sugar—or should one say, catnip?—the library provides for common functional operations, gatos should hopefully make for a fun introduction to concatenative programming.

##Installation (or, “How to Adopt Some Gatos”)
For now, cloning the git repo is the only option.

##Credits
Gatos were developed by William Cybriwsky (twitter@jadeshade, github@riwsky)

I am heavily indebted to Julien Palard’s [Pipe](https://github.com/JulienPalard/Pipe) for showing me how many of these things could be done in Python.

##Further Investigation
If you found this interesting, consider checking out:

- The aforementioned [Pipe](https://github.com/JulienPalard/Pipe), which uses generator expressions instead of pushing and popping from a stack.
- [The Factor Programming Language](http://www.factorcode.org), which as I understand it is the most popular concatenative language right now.
- [Clojure’s “->” macro](http://blog.fogus.me/2009/09/04/understanding-the-clojure-macro/), which drove me to make Gatos in the first place.