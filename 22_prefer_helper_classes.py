'''
1.Avoid making dictionaries with values that are dictionaries or long tuples.
2.Move your bookkeeping code to use multiple helper classes when your internal
  state dictionaries get complicated.
'''
from collections import namedtuple

Grade = namedtuple('Grade', ('score', 'weight'))

class Subject:
    def __init__(self):
        self._grades = []

    def report_grade(self, score, weight):
        self._grades.append(Grade(score, weight))

    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight


class Student:
    def __init__(self):
        self._subjects = {}

    def subject(self, name):
        if name not in self._subjects:
            self._subjects[name] = Subject()
        return self._subjects[name]

    def average_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count


class GradeBook:
    def __init__(self):
        self._students = {}

    def student(self, name):
        if name not in self._students:
            self._students[name] = Student()
        return self._students[name]


book = GradeBook()
albert = book.student('Albert Einstein')
albert.subject('Math').report_grade(80, 0.5)
albert.subject('Math').report_grade(100, 0.5)

print(albert.average_grade())
