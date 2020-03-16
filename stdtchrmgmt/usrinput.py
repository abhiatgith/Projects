# Student Teacher Management System
# Should be able to read and write the data (read and write means should be able to store update delete and read (CRUD)
# Should be flexible enough to choose the number of entries

# Take input from end user
from stdtchrmgmt.classdefs import Student, Teacher
from stdtchrmgmt.classfileops import Fileops

if __name__ == "__main__":
    print("Student/teacher management system")
    print("***********************************")
    print('Enter 1 to Add Student/Teacher data')
    print('Enter 2 to read existing Student/Teacher data')
    print('Enter 3 to update Student/Teacher data')
    print('Enter 4 to delete Student/Teacher data')
    usr_opt = int(input("Enter your option:"))
    # check if user wants to enter new student/teacher data
    if usr_opt == 1:
        new_stu = input("Do you want to enter a student or teacher? Select 'y' for student, 'n' for teacher:")
        # Accept new student data
        if new_stu == 'y':
            while new_stu == 'y':
                student_id = input('Enter Student ID:')
                student_fstname = input('Enter Student First Name:')
                student_lstname = input('Enter Student Last Name:')
                student_coursename = input('Enter Student Course Name:')
                stu1 = Student(student_id,student_fstname,student_lstname,student_coursename,)
                fileop = Fileops('stfile.txt')
                fileop.write_newstu(stu1.id, stu1.fname, stu1.lname, stu1.course)
                new_stu = input("Do you want to enter another student? Select 'y' for yes and 'n' if no:")
        elif new_stu == 'n':
            # Accept new teacher data
            new_tea = 'y'
            while new_tea == 'y':
                teacher_id = input('Enter Teacher ID:')
                teacher_fstname = input('Enter Teacher First Name:')
                teacher_lstname = input('Enter Teacher Last Name:')
                teacher_deptname = input('Enter Teacher Dept Name:')
                tchr1 = Teacher(teacher_id, teacher_fstname, teacher_lstname, teacher_deptname)
                fileop = Fileops('tchrfile.txt')
                fileop.write_newtchr(tchr1.id, tchr1.fname, tchr1.lname, tchr1.dept)
                new_tea = input("Do you want to enter another teacher? Select 'y' for yes and 'n' if no:")
    elif usr_opt == 2:
        # Check if user wants to read student or teacher data
        read_stu = input(
            "Do you want to get details of students or teachers? Select 'y' for student and 'n' for teacher:")
        if read_stu == 'y':
            # Read Student Data
            while read_stu == 'y':
                num_stu = int(input("Select the number of student details that you would like to view:"))
                fileop = Fileops('stfile.txt')
                fileop.read_student(num_stu)
                read_stu = input(
                    "Do you want to get more student details? Select 'y' for yes and 'n' for no:")
        elif read_stu == 'n':
            # Read Teacher Data
            read_tchr = 'y'
            while read_tchr == 'y':
                num_tchr = int(input("Select the number of teacher details that you would like to view:"))
                fileop = Fileops('tchrfile.txt')
                fileop.read_teacher(num_tchr)
                read_tchr = input(
                    "Do you want to get more teacher details? Select 'y' for yes and 'n' for no:")
    elif usr_opt == 3:
            # Check if user wants to update Student or teacher data
            upd_stu = input("Do you want to update details of students or teachers? Select 'y' for student and 'n' "
                            "for teacher:")
            if upd_stu == 'y':
                # Update Student Data
                while upd_stu == 'y':
                    firname = input('Enter Student First Name:')
                    lasname = input('Enter Student Last Name:')
                    upd_what = input('What do you want to update for the student record?, Enter 1 for First Name, '
                                     '2 for Last Name, 3 for Course Name : ')
                    fileop = Fileops('stfile.txt')
                    if int(upd_what) == 1:
                        old_fname = input('Enter Student Old First Name:')
                        new_fname = input('Enter Student New First Name:')
                        fileop.update_rec(firname + ',' + lasname, old_fname, new_fname)
                    elif int(upd_what) == 2:
                        old_lname = input('Enter Student Old Last Name:')
                        new_lname = input('Enter Student New Last Name:')
                        fileop.update_rec(firname + ',' + lasname, old_lname, new_lname)
                    elif int(upd_what) == 3:
                        old_cname = input('Enter Student Old Course Name:')
                        new_cname = input('Enter Student New Course Name:')
                        fileop.update_rec(firname + ',' + lasname, old_cname, new_cname)
                    upd_stu = input(
                        "Do you want to update details for another student? Select 'y' for yes and 'n' for no: ")
            elif upd_stu == 'n':
                upd_tchr = 'y'
                while upd_tchr == 'y':
                    tfirname = input('Enter Teacher First Name:')
                    tlasname = input('Enter Teacher Last Name:')
                    upd_what_tcr = input('What do you want to update for the Teacher record?, Enter 1 for First Name, '
                                         '2 for Last Name, 3 for Dept Name : ')
                    fileop = Fileops('tchrfile.txt')
                    if int(upd_what_tcr) == 1:
                        told_fname = input('Enter Teacher Old First Name:')
                        tnew_fname = input('Enter Teacher New First Name:')
                        fileop.update_rec(tfirname + ',' + tlasname, told_fname, tnew_fname)
                    elif int(upd_what_tcr) == 2:
                        told_lname = input('Enter Teacher Old Last Name:')
                        tnew_lname = input('Enter Teacher New Last Name:')
                        fileop.update_rec(tfirname + ',' + tlasname, told_lname, tnew_lname)
                    elif int(upd_what_tcr) == 3:
                        told_dname = input('Enter Teacher Old Dept Name:')
                        tnew_dname = input('Enter Teacher New Dept Name:')
                        fileop.update_rec(tfirname + ',' + tlasname, told_dname, tnew_dname)
                    upd_tchr = input(
                        "Do you want to update details for another Teacher? Select 'y' for yes and 'n' for no: ")
    elif usr_opt == 4:
                # Check if user wants to delete Student or Teacher data
                del_stu = input("Do you want to delete a student record? Select 'y' for yes, 'n' for teacher:")
                if del_stu == 'y':
                    # Delete Student Data
                    while del_stu == 'y':
                        del_stuf = input('Enter Student First Name:')
                        del_stul = input('Enter Student Last Name:')
                        fileop = Fileops('stfile.txt')
                        fileop.delete_record(del_stuf + ',' + del_stul)
                        del_stu = input(
                            "Do you want to delete another student record? Select 'y' for yes, 'n' for no: ")
                elif del_stu == 'n':
                    # Delete Teacher Data
                    del_tchr = 'y'
                    while del_tchr == 'y':
                        del_tchrf = input('Enter Teacher First Name:')
                        del_tchrl = input('Enter Teacher Last Name:')
                        fileop = Fileops('tchrfile.txt')
                        fileop.delete_record(del_tchrf + ',' + del_tchrl)
                        del_tchr = input(
                            "Do you want to delete another teacher record? Select 'y' for yes, 'n' for no: ")
