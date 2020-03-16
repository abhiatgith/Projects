# Class for file operations

class Fileops:
    def __init__(self, filename):
        self.filename = filename

    # Function to Write student data to student file
    def write_newstu(self, id, fname, lname, course):
        myfile = open(self.filename, 'a+')
        myfile.write(id + ',')
        myfile.write(fname + ',')
        myfile.write(lname + ',')
        myfile.write(course + '\n')
        print('RECORD CREATED')
        print(id, fname, lname, course)
        myfile.close()

    # Function to write teacher data to teacher file
    def write_newtchr(self, id, fname, lname, dept):
        myfile = open(self.filename, 'a+')
        myfile.write(id + ',')
        myfile.write(fname + ',')
        myfile.write(lname + ',')
        myfile.write(dept + '\n')
        print('RECORD CREATED')
        print(id, fname, lname, dept)
        myfile.close()

    # Function to read student data
    def read_student(self, num):
        myfile = open(self.filename, 'r')
        for i in range(num):
            print(myfile.readline(), end='')
        myfile.close()

    # Function to read teacher data
    def read_teacher(self, num):
        myfile = open(self.filename, 'r')
        for i in range(num):
            print(myfile.readline(), end='')
        myfile.close()

    # Function to update student/teacher data

    def update_rec(self, name, word, newword):
        myfile = open(self.filename, 'r')
        lines = myfile.readlines()
        myfile = open(self.filename, 'w+')
        rec_fnd = False
        for line in lines:
            if line.find(name) > -1:
                print('Record Found:' + line)
                rec_fnd = True
                newline = line.replace(word, newword)
                print('Updated Record Details:' + newline)
                myfile.write(newline)
            else:
                myfile.write(line)
        if not rec_fnd:
            print('Record Not Found')
        myfile.close()

    # Function to delete student/teacher data

    def delete_record(self, fullname):
        myfile = open(self.filename, 'r')
        lines = myfile.readlines()
        myfile = open(self.filename, 'w')
        srec_fnd = False
        for line in lines:
            if line.find(fullname) > -1:
                srec_fnd = True
                print(fullname + ' is deleted')
                continue
            myfile.write(line)
        if srec_fnd == False:
            print('Record Not Found')
        myfile.close()
