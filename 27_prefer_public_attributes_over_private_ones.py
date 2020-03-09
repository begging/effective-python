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

