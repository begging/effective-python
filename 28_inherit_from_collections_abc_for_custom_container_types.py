'''
Defining your own container types is much harder than it looks.

To avoid this difficulty throughout the Python universe, the built-in
collections.abc module defines a set of abstract base classes that provide all
of the typical methods for each container type.

When you subclass from these abstract base classes and forget to implement
required methods, the module will tell you something is wrong.
'''
from collections.abc import Sequence

class BadType(Sequence):
    pass

try:
    foo = BadType()
except TypeError as e:
    print(e)



'''
When you do implement all of the methods required by an abstract base class
like __getitem__, __len__, it will provide all of the additional methods like
index and count for free.
'''
