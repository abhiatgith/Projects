# Define the Person class as a parent class and Student and Teacher as child classes

class Person:
    def __init__(self, fname, lname):
        self.fname = fname
        self.lname = lname


class Student(Person):
    def __init__(self, id, fname, lname, course):
        super().__init__(fname, lname)
        self.id = id
        self.course = course


class Teacher(Person):
    def __init__(self, id, fname, lname, dept):
        super().__init__(fname, lname)
        self.id = id
        self.dept = dept


