'''
This is the wrong approach.
By choosing private attributes, you’re only making subclass overrides and
extensions cumbersome and brittle.
'''
class MyClass(object):
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return str(self.__value)

foo = MyClass(5)
print(foo.get_value() == '5')


class MyIntegerSubclass(MyClass):
    def get_value(self):
        return int(self._MyClass__value)

foo = MyIntegerSubclass(5)
assert foo.get_value() == 5



'''
if the class hierarchy changes beneath you, these classes will break because
the private references are no longer valid.

The __value attribute is now assigned in the MyBaseClass parent class, not the
MyClass parent. That causes the private variable reference self._MyClass__value
to break in MyIntegerSubclass.
'''
class MyBaseClass(object):
    def __init__(self, value):
        self.__value = value

class MyClass(MyBaseClass):
    ...

class MyIntegerSubclass(MyClass):
    def get_value(self):
        return int(self._MyClass__value)

foo = MyIntegerSubclass(5)
try:
    foo.get_value()
except AttributeError as e:
    print(e)

'''
In general, it’s better to err on the side of allowing subclasses to do more by
using protected attributes.

Document each protected field and explain which are internal APIs available to
subclasses and which should be left alone entirely.

This is as much advice to other programmers as it is guidance for your future
self on how to extend your own code safely.
'''
class MyClass(object):
    def __init__(self, value):
        # This stores the user-supplied value for the object.
        # It should be coercible to a string.
        # Once assigned for # the object it should be treated as immutable.
        self._value = value


'''
The only time to seriously consider using private attributes is when you’re
worried about naming conflicts with subclasses.

This problem occurs when a child class unwittingly defines an attribute that
was already defined by its parent class.
'''
class ApiClass(object):
    def __init__(self):
        self._value = 5

    def get(self):
        return self._value

class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello'

# Conflicts
a = Child()
print(a.get(), 'and', a._value, 'should be different')



'''
This is primarily a concern with classes that are part of a public API; The
subclasses are out of your control, so you can’t refactor to fix the problem.

Such a conflict is especially possible with attribute names that are very
common (like value).

To reduce the risk of this happening, you can use a private attribute in the
parent class to ensure that there are no attribute names that overlap with
child classes.
'''
class ApiClass(object):
    def __init__(self):
        self.__value = 5

    def get(self):
        return self.__value

class Child(ApiClass):
    def __init__(self):
        super().__init__()
        self._value = 'hello'

# OK!
a = Child()
print(a.get(), 'and', a._value, 'are different')
