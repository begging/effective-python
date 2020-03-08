'''
The old way to initialize a parent class from a child class is to directly call
the parent class’s __init__ method with the child instance.

This approach works fine for simple hierarchies but breaks down in many cases.
'''
class MyBaseClass:
    def __init__(self, value):
        self.value = value

class MyChildClass(MyBaseClass):
    def __init__(self):
        MyBaseClass.__init__(self, 5)


'''
The class AnotherWay's behavior doesn't match the order of the parent classes
in its definition.
'''
class TimesTwo(object):
    def __init__(self):
        self.value *= 2

class PlusFive(object):
    def __init__(self):
        self.value += 5

class AnotherWay(MyBaseClass, PlusFive, TimesTwo):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)


'''
Diamond inheritance causes the common superclass’s __init__ method to run
multiple times, causing unexpected behavior.
'''
class TimesFive(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value *= 5

class PlusTwo(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value += 2

class ThisWay(TimesFive, PlusTwo):
    def __init__(self, value):
        TimesFive.__init__(self, value)
        PlusTwo.__init__(self, value)

foo = ThisWay(5)
print('Should be (5 * 5) + 2 = 27 but is', foo.value)


'''
To solve these problems, Python 2.2 added the super built-in function and
defined the method resolution order (MRO).
The MRO standardizes which superclasses are initialized before others
(e.g., depth-first, left-to-right).

It ensures that common superclasses in diamond hierarchies are only run once.

Now the top part of the diamond, MyBaseClass.__init__, is run a single time.

All of the initialization methods actually do their work in the opposite order
from how their __init__ functions were called.
ex) PlusTwoCorrect.__init__() => TimesFiveCorrect.__init__() in GoodWay.
'''
# Python 2
class TimesFiveCorrect(MyBaseClass):
    def __init__(self, value):
        super(TimesFiveCorrect, self).__init__(value)
        self.value *= 5

class PlusTwoCorrect(MyBaseClass):
    def __init__(self, value):
        super(PlusTwoCorrect, self).__init__(value)
        self.value += 2

class GoodWay(TimesFiveCorrect, PlusTwoCorrect):
    def __init__(self, value):
        super(GoodWay, self).__init__(value)

foo = GoodWay(5)
print('Should be 5 * (5 + 2) = 35 and is', foo.value)


'''
This ordering matches what the MRO defines for this class. The MRO ordering is
available on a class method called mro.
'''
from pprint import pprint
pprint(GoodWay.mro())


'''
The super function works well, but it has two noticeable problems in Python 2:
 - Its syntax is a bit verbose.
 - You have to specify the current class by name in the call to super.
   If you change the class’s name, you also need to update every call to super.

Python 3 fixes these issues by making calls to super witho no arguments
equivalent to calling super with __class__ and self specified.
'''
# Python 3
class Explicit(MyBaseClass):
    def __init__(self, value):
        super(__class__, self).__init__(value * 2)

class Implicit(MyBaseClass):
    def __init__(self, value):
        super().__init__(value * 2)

print(Explicit(10).value == Implicit(10).value)

