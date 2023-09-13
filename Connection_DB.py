import sqlite3

def start():
    global con
    con=sqlite3.connect('System_DB.db')
    
    global cursor
    cursor=con.cursor()


def end():
    con.commit()
    con.close()

def addStudent(ID,Email,Name,Passowrd,Class):
    start()
    cursor.execute('insert into students values (?,?,?,?,?)',(ID,Email,Name,Passowrd,Class))
    end()
  
    
def addTeacher(ID,Email,Name,Passowrd,Class):
    start()
    cursor.execute('insert into teachers values (?,?,?,?,?)',(ID,Email,Name,Passowrd,Class))
    end()
    
    
def searchStudentPassowrdAndEmail(Passowrd,Email):
    start()
    Pass=cursor.execute('SELECT passowrd FROM students WHERE passowrd=? AND Email=? ',(Passowrd,Email))
    Pass=cursor.fetchone()
    end()
    if(Pass==None):
        return False # Not Exist
    else:
       return True
    
    
def searchTeacherPassowrdAndEmail(Passowrd,Email):
    start()
    Pass=cursor.execute('SELECT passowrd FROM teachers WHERE passowrd=? AND Email=? ',(Passowrd,Email))
    Pass=cursor.fetchone()
    end()
    if(Pass==None):
        return False  # Not Exist
    else:
       return True    # Exist
    
    
def searchTeacherId(ID):
    start()
    ID=cursor.execute(f'SELECT ID FROM teachers WHERE ID={ID}')
    ID=cursor.fetchone()
    end()
    if(ID==None):
        return False # This ID Not Exist
    else:
       return True   # This ID Exist
    
def searchTeacherPassowrd(Passowrd):
    start()
    ID=cursor.execute(f'SELECT ID FROM teachers WHERE Passowrd={Passowrd}')
    ID=cursor.fetchone()
    end()
    if(ID==None):
        return False # This Passowrd Not Exist
    else:
       return True   # This Passowrd Exist
    
def searchTeacherEmail(Email):
    start()
    ID=cursor.execute('SELECT ID FROM teachers WHERE Email=?',[Email])
    ID=cursor.fetchone()
    end()
    if(ID==None):
        return False # This Email Not Exist
    else:
       return True   # This Email Exist
    
    
def searchStudentId(ID):
    start()
    ID=cursor.execute(f'SELECT ID FROM students WHERE ID={ID}')
    ID=cursor.fetchone()
    end()
    if(ID==None):
        return False # This ID Not Exist
    else:
       return True   # This ID Exist
    
def searchStudentPassowrd(Passowrd):
    start()
    ID=cursor.execute(f'SELECT ID FROM students WHERE Passowrd={Passowrd}')
    ID=cursor.fetchone()
    end()
    if(ID==None):
        return False # This Passowrd Not Exist
    else:
       return True   # This Passowrd Exist
    
def searchStudentEmail(Email):
    start()
    ID=cursor.execute('SELECT ID FROM students WHERE Email=?',[Email])
    ID=cursor.fetchone()
    end()
    if(ID==None):
        return False # This Email Not Exist
    else:
       return True   # This Email Exist

def getStudentNameAndClass(ID):
    start()
    StudentNameAndClass = cursor.execute(f'SELECT Name,Class FROM students WHERE ID={ID}')
    StudentNameAndClass = cursor.fetchone()
    end()
    return StudentNameAndClass

# =============================================================================
# def searchStudentClass(ID):
#     start()
#     studentClass = cursor.execute(f'SELECT Class FROM students WHERE ID={ID}')
#     studentClass=cursor.fetchone()
#     end()
#     return studentClass
#     
# =============================================================================

def searchTeacherClass(Email,Passowrd):
    start()
    teacherClass = cursor.execute('SELECT Class FROM teachers WHERE Email=? AND Passowrd=?',(Email,Passowrd))
    teacherClass=cursor.fetchone()
    end()
    return teacherClass



# ========================================
def updateStudent(ID,Email,Name,Passowrd,Class):
    start()
    cursor.execute('update students set Email=? , Name=? , Passowrd=? , Class=? where ID=? ',(Email,Name,Passowrd,Class,ID))
    end()
    

def updateTeacher(ID,Email,Name,Passowrd,Class):
    start()
    cursor.execute('update teachers set Email=? , Name=? , Passowrd=? , Class=? where ID=? ',(Email,Name,Passowrd,Class,ID))
    end()    
    
def updateTeacherEmail(ID,Email):
    start()
    cursor.execute('update teachers set Email=? where ID=? ',[Email,ID])
    end()    
    
def updateTeacherName(ID,Name):
    start()
    cursor.execute('update teachers set Name=? where ID=? ',(Name,ID))
    end()
    
def updateTeacherPassowrd(ID,Passowrd):
    start()
    cursor.execute('update teachers set Passowrd=? where ID=? ',(Passowrd,ID))
    end()
    
def updateTeacherClass(ID,Class):
    start()
    cursor.execute('update teachers set Class=? where ID=? ',(Class,ID))
    end()


def updateStudentEmail(ID,Email):
    start()
    cursor.execute('update students set Email=? where ID=? ',[Email,ID])
    end()    
    
def updateStudentName(ID,Name):
    start()
    cursor.execute('update students set Name=? where ID=? ',(Name,ID))
    end()
    
def updateStudentPassowrd(ID,Passowrd):
    start()
    cursor.execute('update students set Passowrd=? where ID=? ',(Passowrd,ID))
    end()
    
def updateStudentClass(ID,Class):
    start()
    cursor.execute('update students set Class=? where ID=? ',(Class,ID))
    end()
    

# ========================================


    
def deleteStudent(ID):
    start()
    cursor.execute(f'delete from students where ID={ID}')
    end()
    
    
def deleteTeacher(ID):
    start()
    cursor.execute(f'delete from teachers where ID={ID}')
    end()
    
    
def searchStudentName(Passowrd,Email):
    start()
    tmp = cursor.execute('SELECT ID,Name FROM students WHERE passowrd=? AND Email=? ',(Passowrd,Email))
    tmp=cursor.fetchone()
    end()
    return tmp


def SearchStudent_ID_Attendence(ID,Class):
    start()
    ID=cursor.execute('SELECT ID FROM attendence WHERE ID=? AND Class=?',(ID,Class))
    ID=cursor.fetchone()
    end()
    if(ID==None):
        return False # This Email Not Exist
    else:
       return True   # This Email Exist
    
    
def totalCalsses(ID):
    start()
    total= cursor.execute(f'SELECT count(*) FROM attendence WHERE ID={ID}')
    total=cursor.fetchone()
    end()
    return total


def AttendedCalsses(ID):
    start()
    attended= cursor.execute('SELECT count(*) FROM attendence WHERE ID=? AND status=?',(ID,'Present'))
    attended=cursor.fetchone()
    end()
    return attended


def MissedCalsses(ID):
    start()
    Missed= cursor.execute('SELECT count(*) FROM attendence WHERE ID=? AND status=?',(ID,'Absent'))
    Missed=cursor.fetchone()
    end()
    return Missed


def addAttend(ID,sName,Datee,status,Class):
    start()
    cursor.execute('insert into attendence values (?,?,?,?,?)',(ID,sName,Datee,status,Class))
    end()    



def updateAttend(ID,Datee,Status):
    start()
    cursor.execute('update attendence set Status=?  where ID=? AND Datee=? ',(Status,ID,Datee))
    end()   



def deleteAttend(ID,Datee):
    start()
    cursor.execute('delete from attendence where ID=? AND Datee=?',(ID,Datee))
    end()
    

def showStudentRecord(ID):
    start()
    data=cursor.execute(f'select Datee,status from attendence where ID={ID}')
    data = cursor.fetchall()
    end()
    return data


def showStudentRecordForTeacher(Class):
    start()
    data=cursor.execute('select * from attendence WHERE Class=?',[Class])
    data = cursor.fetchall()
    end()
    return data
    


def allStudents():
    start()
    data=cursor.execute('select * from students')
    data = cursor.fetchall()
    end()
    return data
    
    
def allTeachers():
    start()
    data=cursor.execute('select * from teachers')
    data = cursor.fetchall()
    end()
    return data
    
# =============================================================================
# 
# def teacherClass(Email):
#     start()
#     Class=cursor.execute('SELECT Class FROM teachers WHERE Email=?',[Email])
#     Class=cursor.fetchone()
#     end()
#     return Class
# =============================================================================
