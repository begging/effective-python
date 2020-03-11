class Field(object):
    def __init__(self, name):
        self.name = name
        self.internal_name = '_' + self.name

    def __get__(self, instance, instance_type):
        if instance is None:
            return self

        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


class Customer(object):

    # Class attributes
    first_name = Field('first_name')
    last_name = Field('last_name')
    prefix = Field('prefix')
    suffix = Field('suffix')


foo = Customer()
print('Before:', repr(foo.first_name), foo.__dict__)
foo.first_name = 'Euclid'
print('After:', repr(foo.first_name), foo.__dict__)
print()



'''
The above example seems redundant. I already declared the name of the field
when I assigned the constructed Field object to Customer.first_name in the
class statement body.

To eliminate the redundancy, I can use a metaclass.
'''
from pprint import pprint
class Meta(type):
    def __new__(meta, name, bases, class_dict):
        print(meta, name, bases)
        pprint(class_dict)
        print()
        for key, value in class_dict.items():
            if isinstance(value, Field):
                value.name = key
                value.internal_name = '_' + key

        cls = type.__new__(meta, name, bases, class_dict)
        return cls


class DatabaseRow(object, metaclass=Meta):
    pass


class Field(object):
    def __init__(self):
        self.name = None
        self.internal_name = None

    def __get__(self, instance, instance_type):
        if instance is None:
            return self

        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


class BetterCustomer(DatabaseRow):
    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()

foo = BetterCustomer()
print('Before:', repr(foo.first_name), foo.__dict__)
foo.first_name = 'Euler'
print('After:', repr(foo.first_name), foo.__dict__)
