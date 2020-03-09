'''
This class is natural and clear.
'''
class Resistor(object):
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0

r1 = Resistor(50e3)
r1.ohms = 10e3
r1.ohms += 5e3


'''
How to use @property and setter
'''
class VoltageResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, value):
        self._voltage = value
        self.current = self._voltage / self.ohms

r2 = VoltageResistance(1e3)
print('Before: %5r amps' % r2.current)
print(r2.voltage)
r2.voltage = 10
print('After: %5r amps' % r2.current)
print(r2.voltage)
print(r2.__dict__)


'''
Specifying a setter on a property also lets you perform type checking and
validation on values passed to your class.
'''
class BoundedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError('%f ohms must be > 0' % ohms)
        self._ohms = ohms

try:
    r3 = BoundedResistance(1e3)
    r3.ohms = 0
except ValueError as e:
    print(e)

try:
    r4 = BoundedResistance(-5)
except ValueError as e:
    print(e)



'''
You can even use @property to make attributes from parent classes immutable.
'''
class FixedResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError('Can’t set attribute')
        self._ohms = ohms

try:
    r4 = FixedResistance(1e3)
    r4.ohms = 2e3
except AttributeError as e:
    print(e)
