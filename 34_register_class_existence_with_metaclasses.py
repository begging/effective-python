import json

class Serializable(object):
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({'args': self.args})


class Point2D(Serializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point2D(%d, %d)' % (self.x, self.y)

point = Point2D(5, 3)
print('Object:', point)
print('Serialized:', point.serialize())
print()


class Deserializable(Serializable):
    @classmethod
    def deserialize(cls, json_data):
        params = json.loads(json_data)
        return cls(*params['args'])


class BetterPoint2D(Deserializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point2D(%d, %d)' % (self.x, self.y)

point = BetterPoint2D(5, 3)
print('Before:', point)
data = point.serialize()
print('Serialized:', data)
after = BetterPoint2D.deserialize(data)
print('After:', after)
print()


'''
The problem with this approach is that it only works if you know the intended
type of the serialized data ahead of time (e.g., Point2D, BetterPoint2D).

Ideally, you’d have a large number of classes serializing to JSON and one
common function that could deserialize any of them back to a corresponding
Python object.

To do this, I can include the serialized object’s class name in the JSON data.
'''
class BetterSerializable(object):
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args': self.args, })

    def __repr__(self):
        return 'Point2D(%d, %d)' % (self.x, self.y)


registry = {}

def register_class(target_class):
    registry[target_class.__name__] = target_class

def deserialize(data):
    params = json.loads(data)
    name = params['class']
    target_class = registry[name]
    return target_class(*params['args'])

class EvenBetterPoint2D(BetterSerializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

register_class(EvenBetterPoint2D)

point = EvenBetterPoint2D(5, 3)
print('Before:', point)
data = point.serialize()
print('Serialized:', data)
after = deserialize(data)
print('After:', after)



'''
The problem with this approach is that you can forget to call register_class.

This will cause your code to break at runtime, when you finally try to
deserialize an object of a class you forgot to register.

What if you could somehow act on the programmer’s intent to use
BetterSerializable and ensure that register_class is called in all cases?

Metaclasses enable this by intercepting the class statement when subclasses are
defined.

This lets you register the new type immediately after the class’s body.
'''
class Meta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        print(meta, name, bases, class_dict)
        register_class(cls)
        return cls


class RegisteredSerializable(BetterSerializable, metaclass=Meta):
    pass


class Vector3D(RegisteredSerializable):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x, self.y, self.z = x, y, z


v3 = Vector3D(10, -7, 3)
print('Before:', v3)
data = v3.serialize()
print('Serialized:', data)
print('After:', deserialize(data))

print(registry)
