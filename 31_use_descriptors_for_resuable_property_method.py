'''
Say you also want to give the student a grade for an exam, where the exam has
multiple subjects, each with a separate grade.

Each section of the exam requires adding a @property and related validation.

So this approach is not general.
'''
class Exam(object):
    def __init__(self):
        self._writing_grade = 0
        self._math_grade = 0

    @staticmethod
    def _check_grade(value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')

    @property
    def writing_grade(self):
        return self._writing_grade

    @writing_grade.setter
    def writing_grade(self, value):
        self._check_grade(value)
        self._writing_grade = value

    @property
    def math_grade(self):
        return self._math_grade

    @math_grade.setter
    def math_grade(self, value):
        self._check_grade(value)
        self._math_grade = value



'''
The better way to do this in Python is to use a descriptor.

A descriptor class can provide __get__ and __set__ methods that let you reuse
the grade validation behavior without any boilerplate.

For this purpose, descriptors are also better than mix-ins because they let you
reuse the same logic for many different attributes in a single class.
'''
class Grade(object):
    def __init__(self):
        self._value = 0

    def __get__(self, instance, instance_type):
        return self._value

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._value = value


class Exam(object):
    # Class attributes
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

first_exam = Exam()
first_exam.writing_grade = 82
first_exam.science_grade = 99
print('Writing', first_exam.writing_grade)
print('Science', first_exam.science_grade)

second_exam = Exam()
second_exam.writing_grade = 75
print('Second', second_exam.writing_grade, 'is right')
print('First', first_exam.writing_grade, 'is wrong')



'''
The problem is that a single Grade instance is shared across all Exam instances
for the class attribute writing_grade.

The Grade instance for this attribute is constructed once in the program
lifetime when the Exam class is first defined, not each time an Exam instance
is created.

To solve this, I need the Grade class to keep track of its value for each
unique Exam instance.
I can do this by saving the per-instance state in a dictionary.
'''
class Grade(object):
    def __init__(self):
        self._values = {}

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance] = value


'''
The above Grade class leaks memoery.

The _values dictionary will hold a reference to every instance of Exam ever
passed to __set__ over the lifetime of the program.

This causes instances to never have their reference count go to zero,
preventing cleanup by the garbage collector.

To fix this, I can use Python’s weakref built-in module.
This module provides a special class called WeakKeyDictionary that can take the
place of the simple dictionary used for _values.

The unique behavior of WeakKeyDictionary is that it will remove Exam instances
from its set of keys when the runtime knows it’s holding the instance’s last
remaining reference in the program.
'''
from weakref import WeakKeyDictionary

class Grade(object):
    def __init__(self):
        # self._values = {}
        self._values = WeakKeyDictionary()

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance] = value


class Exam(object):
    # Class attributes
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()


first_exam = Exam()
first_exam.writing_grade = 82
second_exam = Exam()
second_exam.writing_grade = 75
print('First', first_exam.writing_grade, 'is right')
print('Second', second_exam.writing_grade, 'is right')
print(first_exam.__dict__)
print(second_exam.__dict__)


'''
If I define grade attributes as instances of Grade(), these __get__, __set__
method doesn't work.

In short, when an Exam instance doesn’t have an attribute named writing_grade,
Python will fall back to the Exam class’s attribute instead.

If this class attribute is an object that has __get__ and __set__ methods,
Python will assume you want to follow the descriptor protocol.
'''
from weakref import WeakKeyDictionary

class Grade(object):
    def __init__(self):
        # self._values = {}
        self._values = WeakKeyDictionary()

    def __get__(self, instance, instance_type):
        print(instance)
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        print(instance)
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance] = value


class Exam(object):
    # Class attributes
    def __init__(self):
        self.math_grade = Grade()
        self.writing_grade = Grade()
        self.science_grade = Grade()

first_exam = Exam()
first_exam.writing_grade = 82
second_exam = Exam()
second_exam.writing_grade = 75
print('First', first_exam.writing_grade, 'is right')
print('Second', second_exam.writing_grade, 'is right')

print(first_exam.__dict__)
