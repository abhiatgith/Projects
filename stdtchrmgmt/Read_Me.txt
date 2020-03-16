Student/Teacher Management program - Readme file

1. 'usrinput.py' is the main program
2.  We get user input in the 'usrinput.py' program.
3.  Once we get the user input, we instantiate the appropriate class (Student/teacher depending on user input) and then call the appropriate action to perform function (for the CRUD operation to be performed) from the Fileops class.
4.  'classdefs.py' has the details of the parent class' Person' and the child classes student and Teacher.
5.  'classfileops.py' has details of the Fileops class where I have defined functions for each file operations that needs to be performed. For Update and Delete operations, I have a common function that is called for both the student and teacher.
