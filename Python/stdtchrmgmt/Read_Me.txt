Project Name: Student/Teacher Management System

Project Description:
A python project to explore and implement a basic student and teacher management system by incorporating modular and object oriented concepts.
Requirements:
- Should be able to Create, Read, Update and delete (CRUD) student and teacher details
- Should be flexible enough to choose the number of entries

Project Files and Execution flow:

1. 'usrinput.py' is the main program
2. We get user input in the 'usrinput.py' program.
3. Once we get the user input, we instantiate the appropriate class (Student/teacher depending on user input) and then call the appropriate function to perform appropriate CRUD operation to be performed from the Fileops class.
4. The Student details are recorded in the stfile.txt and the teacher details are recorded in the tchrfile.txt
4. 'classdefs.py' has the details of the parent class' Person' and the child classes student and Teacher.
5. 'classfileops.py' has details of the Fileops class where I have defined functions for each file operations that needs to be performed. For Update and Delete operations, I have a common function that is called for both the student and teacher.

