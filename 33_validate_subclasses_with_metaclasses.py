class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
    # Don’t validate the abstract Polygon class
        print((meta, name, bases, class_dict))
        if bases != (object,):
            if class_dict['sides'] < 3:
                raise ValueError('Polygons need 3+ sides')

        return type.__new__(meta, name, bases, class_dict)


class Polygon(object, metaclass=ValidatePolygon):
    sides = None
    # Specified by subclasses

    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180


class Triangle(Polygon):
    sides = 3


'''
The __new__ method of metaclasses is run after the class statement’s entire
body has been processe
'''
class Line(Polygon):
    print('Before sides')
    sides = 1
    print('After sides')

print('After class')
