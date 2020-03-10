'''
If your class defines __getattr__, that method is called every time an
attribute can’t be found in an object’s instance dictionary.
'''
class Test(object):
    def __init__(self):
        self.a = 0

    def __getattr__(self, name):
        print('__getattr__')
        #super().__getattr__(name)

test = Test()
print(hasattr(test, 'b'))
print()


'''
The exists attribute is present in the instance dictionary, so __getattr__ is
never called for it.

The foo attribute is not in the instance dictionary initially, so __getattr__
is called the first time.

This behavior is especially helpful for use cases like lazily accessing
schemaless data.

__getattr__ runs once to do the hard work of loading a property; all subsequent
accesses retrieve the existing result.
'''
class LazyDB(object):
    def __init__(self):
        self.exists = 5

    def __getattr__(self, name):
        value = 'Value for %s' % name
        setattr(self, name, value)
        return value


data = LazyDB()
print('Before:', data.__dict__)
print('foo:', data.foo)
print('After:', data.__dict__)
print()


class LoggingLazyDB(LazyDB):
    def __getattr__(self, name):
        print('Called __getattr__(%s)' % name)
        return super().__getattr__(name)

data = LoggingLazyDB()
print('exists:', data.exists)
print('foo:' , data.foo)
print('foo:', data.foo)
print()


'''
Python has another language hook called __getattribute__. This special method
is called every time an attribute is accessed on an object, even in cases
where it does exist in the attribute dictionary.
'''
class ValidatingDB(object):
    def __init__(self):
        self.exists = 5

    def __getattribute__(self, name):
        print('Called __getattribute__(%s)' % name)
        try:
            return super().__getattribute__(name)
        except AttributeError:
            value = 'Value for %s' % name
            setattr(self, name, value)
            return value

data = ValidatingDB()
print('exists:', data.exists)
print('foo:', data.foo)
print('foo:', data.foo)



'''
Python code implementing generic functionality often relies on the hasattr
built-in function to determine when properties exist, and the getattr built-in
function to retrieve property values.

These functions also look in the instance dictionary for an attribute name
before calling __getattr__.
'''
data = LoggingLazyDB()
print('Before:', data.__dict__)
# How do I make this false? actually data instance has no 'foo' attribute.
print('foo exists:', hasattr(data, 'foo'))
print('After:', data.__dict__)
print('foo exists:', hasattr(data, 'foo'))
print()


'''
In the example above, __getattr__ is only called once. In contrast, classes
that implement __getattribute__ will have that method called each time hasattr
or getattr is run on an object.
'''
data = ValidatingDB()
print('foo exists:', hasattr(data, 'foo'))
print('foo exists:', hasattr(data, 'foo'))
