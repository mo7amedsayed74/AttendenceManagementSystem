from tkinter import *
from tkinter.ttk import Combobox
import tkinter.messagebox
from tkinter.ttk import Treeview
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import Connection_DB



def StudentScreen(StudentData):
    student=Tk()
    student.title('Student')
    w=600
    h=400
    student.geometry(f'{w}x{h}')
    student.configure(bg='darkslategray')
    student.resizable(False,False)
    ##left frame##
    leftframe=Frame(student)
    leftframe['bg']='darkslategray'


    welcome_lbl=Label(leftframe,text=f'Welcome {StudentData[1]},',bg='darkslategray',fg='white')
    welcome_lbl.grid(row=0,column=0 ,padx=10,pady=30)


    total_lbl=Label(leftframe,text='Total Classes:',bg='darkslategray',fg='white')
    total_lbl.grid(row=1,column=0,padx=10,pady=30)

    total=Connection_DB.totalCalsses(StudentData[0])
    tot_lbl=Label(leftframe,text=f'{total[0]}',bg='darkslategray',fg='white')
    tot_lbl.grid(row=1,column=1,padx=10,pady=30)


    attended_lbl=Label(leftframe,text='Attended :',bg='darkslategray',fg='white')
    attended_lbl.grid(row=2,column=0,padx=10,pady=30)

    attended=Connection_DB.AttendedCalsses(StudentData[0])
    att_lbl=Label(leftframe,text=f'{attended[0]}',bg='darkslategray',fg='white')
    att_lbl.grid(row=2,column=1,padx=10,pady=30)


    missed_lbl=Label(leftframe,text='Missed :',bg='darkslategray',fg='white')
    missed_lbl.grid(row=3,column=0,padx=10,pady=30)

    Missed=Connection_DB.MissedCalsses(StudentData[0])
    miss_lbl=Label(leftframe,text=f'{Missed[0]}',bg='darkslategray',fg='white')
    miss_lbl.grid(row=3,column=1,padx=10,pady=30)

    leftframe.pack(side='left')


    data = Connection_DB.showStudentRecord(StudentData[0])
     
    #right frame
    right_frame = Frame(student)
    right_frame.pack(side='right',padx=20  )
    treeview = Treeview(right_frame, columns=('Date', 'Statues'), show='headings')
    treeview.heading('Date', text='Date')
    treeview.heading('Statues', text='Status')

    for row in data:
        treeview.insert('',END,values=row)
        
    treeview.pack()

    student.mainloop()
       

def TeacherScreen(teacherClass):
    selected_item = None  # Global variable to store the selected item

    def add_details():
        id_val = id_entry.get()
        #name_val = name_entry.get()
        date_val = date_entry.get()
        choice = Rbt_var.get()
        #data = (id_val, name_val, date_val, choice)
        if(len(id_val)==0 or len(str(date_val))==0 or len(choice)==0): # or len(str(name_val))==0 
           messagebox.showerror('error','All Data is Required, Please Enter Your Data')
        else :
            flag=Connection_DB.searchStudentId(id_val)
            if(flag==False): # check if student Exist or Not
                messagebox.showwarning('Wornning!','This Student Does not Exist')
            else:
                StudentNameAndClass = Connection_DB.getStudentNameAndClass(id_val)
# =============================================================================
#                 print(StudentNameAndClass)
#                 print(teacherClass)
#                 print(StudentNameAndClass[1])
# =============================================================================
                if(teacherClass[0] == StudentNameAndClass[1]):
                    studentName = StudentNameAndClass[0]
                    studentData = (id_val,studentName , date_val, choice)
                    treeview.insert('', 'end', values=studentData)
                    Connection_DB.addAttend(id_val,studentName,date_val,choice,StudentNameAndClass[1])
                    messagebox.showinfo('System','Added successfully')
                    clear_details()
                else:
                    messagebox.showwarning('Wornning!','This Student Does not Exist in Your Class')
                
                
                
        
        
    def edit_details():
        global selected_item
        selected_item = treeview.selection()
        if len(selected_item) > 0:
            item_values = treeview.item(selected_item)['values']
            id_entry.delete(0, 'end')
            id_entry.insert(0, item_values[0])
# =============================================================================
#             name_entry.delete(0, 'end')
#             name_entry.insert(0, item_values[1])
# =============================================================================
            date_entry.delete(0, 'end')
            date_entry.insert(0, item_values[2])
            Rbt_var.set(item_values[3])
            edit_button.config(command=update_details)  # Remove lambda and selected_item parameter
        else:
            messagebox.showwarning('Wornning','select any item to edit it')

    def update_details():
        global selected_item  # Add global keyword
        id_val = id_entry.get()
        #name_val = name_entry.get()
        date_val = date_entry.get()
        status_val = Rbt_var.get()
        
        StudentNameAndClass = Connection_DB.getStudentNameAndClass(id_val)
        
        treeview.item(selected_item, values=(id_val, StudentNameAndClass[0], date_val, status_val))
        Connection_DB.updateAttend(id_val,date_val, status_val)
        messagebox.showinfo('System','Edit Successfully')
        clear_details()


    def delete_details():
        selected_item = treeview.selection()
        if len(selected_item) > 0:
            item_values = treeview.item(selected_item)['values']
            id_teh=item_values[0]
            Datee = item_values[2]
            Connection_DB.deleteAttend(id_teh,Datee)
            treeview.delete(selected_item)
            messagebox.showinfo('System','Deleted Successfully')
        else:  
           id_val = id_entry.get()
           if(len(id_val)==0):
                messagebox.showerror('error','Required Data, Please Enter Your Data')
           else: 
               flag = Connection_DB.searchStudentId(id_val)
               if(flag==False): # check if student Exist or Not
                   messagebox.showwarning('Wornning!','This Student Does not Exist')
               else:
                   StudentNameAndClass = Connection_DB.getStudentNameAndClass(id_val)
                   if(teacherClass[0] == StudentNameAndClass[1]):
                       Connection_DB.deleteAttend(id_val)
                       messagebox.showinfo('System','Deleted Successfully')
                   else:
                       messagebox.showwarning('Wornning!','This Student Does not Exist in Your Class')
        

    def showRecords():
        id_val = id_entry.get()
        flagExist = Connection_DB.SearchStudent_ID_Attendence(id_val,teacherClass[0])
        if(flagExist == False):
            messagebox.showerror('Wornning!','This ID does not Exist')
        else:
            total=Connection_DB.totalCalsses(id_val)
            attended=Connection_DB.AttendedCalsses(id_val)
            Missed=Connection_DB.MissedCalsses(id_val)
            messagebox.askokcancel('Student Records',f'Total Classes is : {total[0]} , Attended is : {attended[0]} , Missed is : {Missed[0]}')
          



    def clear_details():
        id_entry.delete(0, 'end')
        #name_entry.delete(0, 'end')
        date_entry.delete(0, 'end')
        Rbt_var.set('Present')

    teacher_manage_attendence = tk.Tk()
    teacher_manage_attendence.title('User Details')
    teacher_manage_attendence.geometry('1050x400')
    teacher_manage_attendence.configure(bg='darkslategray')

    # Left Frame
    left_frame = ttk.Frame(teacher_manage_attendence)
    left_frame.pack(side='left', padx=10, pady=10)

    id_label = ttk.Label(left_frame, text='ID:')
    id_label.grid(row=0, column=0, sticky='w')
    id_entry = ttk.Entry(left_frame)
    id_entry.grid(row=0, column=1)
# =============================================================================
# 
#     name_label = ttk.Label(left_frame, text='Name:')
#     name_label.grid(row=2, column=0, sticky='w')
#     name_entry = ttk.Entry(left_frame)
#     name_entry.grid(row=2, column=1)
# 
# =============================================================================
    date_label = ttk.Label(left_frame, text='Date:')
    date_label.grid(row=3, column=0, sticky='w')
    date_entry = ttk.Entry(left_frame)
    date_entry.grid(row=3, column=1)

    Rbt_var = StringVar()
    Rbt_var.set('Present')
    rd1 = Radiobutton(left_frame, text='Absent', value='Absent', variable=Rbt_var)
    rd1.grid(row=5, column=1, pady=5, sticky='w')

    rd2 = Radiobutton(left_frame, text='Present', value='Present', variable=Rbt_var)
    rd2.grid(row=5, column=0, pady=5, sticky='w')

    add_button = ttk.Button(left_frame, text='Add', command=add_details)
    add_button.grid(row=6, column=0, pady=10)

    edit_button = ttk.Button(left_frame, text='Edit', command=edit_details)
    edit_button.grid(row=6, column=1, pady=10)

    delete_button = ttk.Button(left_frame, text='Delete', command=delete_details)
    delete_button.grid(row=7, column=0, pady=10)

    clear_button = ttk.Button(left_frame, text='Records', command=showRecords)
    clear_button.grid(row=7, column=1, pady=10)

    # Right Frame
    right_frame = ttk.Frame(teacher_manage_attendence)
    right_frame.pack(side='right', padx=10, pady=10)
    treeview = ttk.Treeview(right_frame, columns=('ID', 'Name', 'Date', 'Status'), show='headings')
    treeview.heading('ID', text='ID')
    treeview.heading('Name', text='Name')
    treeview.heading('Date', text='Date')
    treeview.heading('Status', text='Status')
    
    #print(teacherClass[0])
    
    Records = Connection_DB.showStudentRecordForTeacher(teacherClass[0])
    if(Records!=None):
        for row in Records:
            treeview.insert('',END,values=row)
            
    treeview.pack()

    teacher_manage_attendence.mainloop()


def StudentControlModuleScreen():
    def add_details():
        id_val = id_entry.get()
        email_val = email_entry.get()
        name_val = name_entry.get()
        password_val = password_entry.get()
        class_val = class_comboBox.get()
        data = (id_val, email_val, name_val, password_val, class_val)
        
        if(len(id_val)==0 or len(str(email_val))==0 or len(str(name_val))==0 or len(password_val)==0 or len(str(class_val))==0):
           messagebox.showerror('Wornning!','All Data is Required, Please Enter Your Data')
        else :
            flagID = Connection_DB.searchStudentId(id_val)
            if(flagID==True): # This ID is Already Exist
                messagebox.showerror('Wornning!','Invalid ID , Try Again!')
            
            flagPassowrd = Connection_DB.searchStudentPassowrd(password_val)
            if(flagPassowrd==True): # This Passowd is Already Exist
                messagebox.showerror('Wornning!','Invalid Passowrd , Try Again!')
            
            flagEmail = Connection_DB.searchStudentEmail(email_val)
            if(flagEmail==True): # This Email is Already Exist
                messagebox.showerror('Wornning!','Invalid Email , Try Again!')
            
            if(flagID==False and flagPassowrd==False and flagEmail==False):
                treeview.insert('', 'end', values=data)
                Connection_DB.addStudent(id_val,email_val,name_val, password_val,class_val)
                messagebox.showinfo('System','Added successfully')
                resetValues()


    # Display new updated tree view 
    def updateTreeView():
        students = Connection_DB.allStudents()
        # remove tree view from other display
        treeview.delete(*treeview.get_children())
        for row in students:
            treeview.insert('',END,values=row)
            
            
    def edit_details():
        selected_item = treeview.selection()
        if len(selected_item) > 0:
            item_values = treeview.item(selected_item)['values']
            id_entry.delete(0, 'end')
            id_entry.insert(0, item_values[0])
            email_entry.delete(0, 'end')
            email_entry.insert(0, item_values[1])
            name_entry.delete(0, 'end')
            name_entry.insert(0, item_values[2])
            password_entry.delete(0, 'end')
            password_entry.insert(0, item_values[3])
            class_comboBox.set(item_values[4])
            # Update the command of the "Edit" button to call a different function
            edit_button.config(command=lambda: update_details(selected_item))
        else:
            id_val = id_entry.get()
            email_val = email_entry.get()
            name_val = name_entry.get()
            password_val = password_entry.get()
            class_val = class_comboBox.get()
            if(len(id_val)==0):
               messagebox.showerror('error','you should enter correct ID')
            else:   
                flagID = Connection_DB.searchStudentId(id_val)
                if(flagID==False): # Does not Exist
                     messagebox.showerror("error","This ID is not Exist")
                else: # ID is Exist
                    if(len(str(email_val)) > 0):
                        Connection_DB.updateStudentEmail(id_val, email_val)
                    if(len(str(name_val)) > 0):
                        Connection_DB.updateStudentName(id_val, name_val)
                    if(len(password_val) > 0):
                        Connection_DB.updateStudentPassowrd(id_val, password_val)
                    if(len(str(class_val)) > 0):
                        Connection_DB.updateStudentClass(id_val, class_val)
                        
                    updateTreeView()
                    messagebox.showinfo('System','Updeted successfully')
                    resetValues()

    # Add a new function to update the details
    def update_details(selected_item):
        id_val = id_entry.get()
        email_val = email_entry.get()
        name_val = name_entry.get()
        password_val = password_entry.get()
        class_val = class_comboBox.get()
        Connection_DB.updateStudent(id_val,email_val,name_val,password_val,class_val)
        # Update the values in the treeview
        treeview.item(selected_item, values=(id_val, email_val, name_val, password_val, class_val))
        # Clear the entry fields
        messagebox.showinfo('System','Updeted successfully')
        resetValues()

    def delete_details():
        selected_item = treeview.selection()
        if len(selected_item) > 0:
            item_values = treeview.item(selected_item)['values']
            id_student=item_values[0]
            Connection_DB.deleteStudent(id_student)
            treeview.delete(selected_item)
            messagebox.showinfo('System','Deleted successfully')
            resetValues()
        else:  
           id_val = id_entry.get()
           if(len(id_val)==0):
                messagebox.showerror('error','Required Data, Please Enter Your Data')
           else: 
                 Connection_DB.deleteStudent(id_val)
                 updateTreeView()
                 messagebox.showinfo('System','Deleted successfully')
                 resetValues()

    def resetValues():
        id_entry.delete(0, 'end')
        email_entry.delete(0, 'end')
        name_entry.delete(0, 'end')
        password_entry.delete(0, 'end')
        class_comboBox.set('')

    def go_back():
        student_control_module.destroy()
        AdminScreen()
        

    student_control_module = tk.Tk()
    student_control_module.title('Student Control Module')
    student_control_module.geometry('1250x400')
    student_control_module.configure(bg='darkslategray')

    # Left Frame
    left_frame = ttk.Frame(student_control_module)
    left_frame.pack(side='left', padx=10, pady=10)

    id_label = ttk.Label(left_frame, text='ID:')
    id_label.grid(row=0, column=0, sticky='w')
    id_entry = ttk.Entry(left_frame)
    id_entry.grid(row=0, column=1)

    email_label = ttk.Label(left_frame, text='Email:')
    email_label.grid(row=1, column=0, sticky='w')
    email_entry = ttk.Entry(left_frame)
    email_entry.grid(row=1, column=1)

    name_label = ttk.Label(left_frame, text='Name:')
    name_label.grid(row=2, column=0, sticky='w')
    name_entry = ttk.Entry(left_frame)
    name_entry.grid(row=2, column=1)

    password_label = ttk.Label(left_frame, text='Password:')
    password_label.grid(row=3, column=0, sticky='w')
    password_entry = ttk.Entry(left_frame, show='*')
    password_entry.grid(row=3, column=1)

    class_label = ttk.Label(left_frame, text='Class:')
    class_label.grid(row=4, column=0, sticky='w')

    class_vars = ['CS', 'SC', 'AI', 'IS']
    class_comboBox = ttk.Combobox(left_frame, values=class_vars, state='readonly')
    class_comboBox.grid(row=4, column=1)

    add_button = ttk.Button(left_frame, text='Add', command=add_details)
    add_button.grid(row=5, column=0, pady=10)

    edit_button = ttk.Button(left_frame, text='Edit', command=edit_details)
    edit_button.grid(row=5, column=1, pady=10)

    delete_button = ttk.Button(left_frame, text='Delete', command=delete_details)
    delete_button.grid(row=6, column=0, pady=10)

    clear_button = ttk.Button(left_frame, text='Reset', command=resetValues)
    clear_button.grid(row=6, column=1, pady=10)

    back_button = ttk.Button(left_frame, text='Back', command=go_back)
    back_button.grid(row=7, column=0, columnspan=2, pady=10)

    # Right Frame
    right_frame = ttk.Frame(student_control_module)
    right_frame.pack(side='right', padx=10, pady=10)
    treeview = ttk.Treeview(right_frame, columns=('ID', 'Email', 'Name', 'Password', 'Class'), show='headings')
    treeview.heading('ID', text='ID')
    treeview.heading('Email', text='Email')
    treeview.heading('Name', text='Name')
    treeview.heading('Password', text='Password')
    treeview.heading('Class', text='Class')
    
    data =Connection_DB.allStudents()
    for row in data:
        treeview.insert('',END,values=row)
    treeview.pack()

    student_control_module.mainloop()


def TeacherControlModuleScreen():
    def add_details():
        id_val = id_entry.get()
        email_val = email_entry.get()
        name_val = name_entry.get()
        password_val = password_entry.get()
        class_val = class_comboBox.get()
        data = (id_val, email_val, name_val, password_val, class_val)
        
        if(len(id_val)==0 or len(str(email_val))==0 or len(str(name_val))==0 or len(password_val)==0 or len(str(class_val))==0):
           messagebox.showerror('Wornning!','All Data is Required, Please Enter Your Data')
        else :
            flagID = Connection_DB.searchTeacherId(id_val)
            if(flagID==True): # This ID is Already Exist
                messagebox.showerror('Wornning!','Invalid ID , Try Again!')
            
            flagPassowrd = Connection_DB.searchTeacherPassowrd(password_val)
            if(flagPassowrd==True): # This Passowd is Already Exist
                messagebox.showerror('Wornning!','Invalid Passowrd , Try Again!')
            
            flagEmail = Connection_DB.searchTeacherEmail(email_val)
            if(flagEmail==True): # This Email is Already Exist
                messagebox.showerror('Wornning!','Invalid Email , Try Again!')
            
            if(flagID==False and flagPassowrd==False and flagEmail==False):
                treeview.insert('', 'end', values=data)
                Connection_DB.addTeacher(id_val,email_val,name_val, password_val,class_val)
                messagebox.showinfo('System','Added successfully')
                resetValues()


    # Display new updated tree view 
    def updateTreeView():
        teachers = Connection_DB.allTeachers()
        #remove tree view from other display
        treeview.delete(*treeview.get_children())
        for row in teachers:
            treeview.insert('',END,values=row)
            
            
    def edit_details():
        selected_item = treeview.selection()
        if len(selected_item) > 0:
            item_values = treeview.item(selected_item)['values']
            id_entry.delete(0, 'end')
            id_entry.insert(0, item_values[0])
            email_entry.delete(0, 'end')
            email_entry.insert(0, item_values[1])
            name_entry.delete(0, 'end')
            name_entry.insert(0, item_values[2])
            password_entry.delete(0, 'end')
            password_entry.insert(0, item_values[3])
            class_comboBox.set(item_values[4])
            # Update the command of the "Edit" button to call a different function
            edit_button.config(command=lambda: update_details(selected_item))
        else:
            id_val = id_entry.get()
            email_val = email_entry.get()
            name_val = name_entry.get()
            password_val = password_entry.get()
            class_val = class_comboBox.get()
            
            if(len(id_val)==0):
               messagebox.showerror('error','you should enter ID')
            else:   
                f=Connection_DB.searchTeacherId(id_val)
                if(f==False): # Does not Exist
                    messagebox.showerror('error','you should enter correct ID')
                else: # ID is Exist
                    if(len(str(email_val)) > 0):
                        Connection_DB.updateTeacherEmail(id_val, email_val)
                    if(len(str(name_val)) > 0):
                        Connection_DB.updateTeacherName(id_val, name_val)
                    if(len(password_val) > 0):
                        Connection_DB.updateTeacherPassowrd(id_val, password_val)
                    if(len(str(class_val)) > 0):
                        Connection_DB.updateTeacherClass(id_val, class_val)
                        
                    updateTreeView()
                    messagebox.showinfo('System','Updeted successfully')
                    resetValues()
                    
    # Add a new function to update the details
    def update_details(selected_item):
        id_val = id_entry.get()
        email_val = email_entry.get()
        name_val = name_entry.get()
        password_val = password_entry.get()
        class_val = class_comboBox.get()
        Connection_DB.updateTeacher(id_val,email_val,name_val,password_val,class_val)
        # Update the values in the treeview
        treeview.item(selected_item, values=(id_val, email_val, name_val, password_val, class_val))
        # Clear the entry fields
        messagebox.showinfo('System','Updeted successfully')
        resetValues()

    def delete_details():
        selected_item = treeview.selection()
        if len(selected_item) > 0:
            item_values = treeview.item(selected_item)['values']
            id_teh=item_values[0]
            Connection_DB.deleteTeacher(id_teh)
            treeview.delete(selected_item)
            messagebox.showinfo('System','Deleted successfully')
            resetValues()
        else:  
           id_val = id_entry.get()
           if(len(id_val)==0):
                messagebox.showerror('error','Required Data, Please Enter Your ID')
           else: 
                flagID=Connection_DB.searchTeacherId(id_val)
                if(flagID==False):
                    messagebox.showerror('Wornning!','Already Not Exist')
                     
                Connection_DB.deleteTeacher(id_val)
                updateTreeView()
                messagebox.showinfo('System','Deleted successfully')
                resetValues()

    def resetValues():
        id_entry.delete(0, 'end')
        email_entry.delete(0, 'end')
        name_entry.delete(0, 'end')
        password_entry.delete(0, 'end')
        class_comboBox.set('')

    def go_back():
        teacher_control_module.destroy()
        AdminScreen()
        

    teacher_control_module = tk.Tk()
    teacher_control_module.title('Teacher Control Module')
    teacher_control_module.geometry('1250x400')
    teacher_control_module.configure(bg='darkslategray')

    # Left Frame
    left_frame = ttk.Frame(teacher_control_module)
    left_frame.pack(side='left', padx=10, pady=10)

    id_label = ttk.Label(left_frame, text='ID:')
    id_label.grid(row=0, column=0, sticky='w')
    id_entry = ttk.Entry(left_frame)
    id_entry.grid(row=0, column=1)

    email_label = ttk.Label(left_frame, text='Email:')
    email_label.grid(row=1, column=0, sticky='w')
    email_entry = ttk.Entry(left_frame)
    email_entry.grid(row=1, column=1)

    name_label = ttk.Label(left_frame, text='Name:')
    name_label.grid(row=2, column=0, sticky='w')
    name_entry = ttk.Entry(left_frame)
    name_entry.grid(row=2, column=1)

    password_label = ttk.Label(left_frame, text='Password:')
    password_label.grid(row=3, column=0, sticky='w')
    password_entry = ttk.Entry(left_frame, show='*')
    password_entry.grid(row=3, column=1)

    class_label = ttk.Label(left_frame, text='Class:')
    class_label.grid(row=4, column=0, sticky='w')

    class_vars = ['CS', 'SC', 'AI', 'IS']
    class_comboBox = ttk.Combobox(left_frame, values=class_vars, state='readonly')
    class_comboBox.grid(row=4, column=1)

    add_button = ttk.Button(left_frame, text='Add', command=add_details)
    add_button.grid(row=5, column=0, pady=10)

    edit_button = ttk.Button(left_frame, text='Edit', command=edit_details)
    edit_button.grid(row=5, column=1, pady=10)

    delete_button = ttk.Button(left_frame, text='Delete', command=delete_details)
    delete_button.grid(row=6, column=0, pady=10)

    clear_button = ttk.Button(left_frame, text='Reset', command=resetValues)
    clear_button.grid(row=6, column=1, pady=10)

    back_button = ttk.Button(left_frame, text='Back', command=go_back)
    back_button.grid(row=7, column=0, columnspan=2, pady=10)

    # Right Frame
    right_frame = ttk.Frame(teacher_control_module)
    right_frame.pack(side='right', padx=10, pady=10)
    treeview = ttk.Treeview(right_frame, columns=('ID', 'Email', 'Name', 'Password', 'Class'), show='headings')
    treeview.heading('ID', text='ID')
    treeview.heading('Email', text='Email')
    treeview.heading('Name', text='Name')
    treeview.heading('Password', text='Password')
    treeview.heading('Class', text='Class')
    
    data =Connection_DB.allTeachers()
    for row in data:
        treeview.insert('',END,values=row)
    treeview.pack()

    teacher_control_module.mainloop()


def AdminScreen():
    admin = Tk()        
    admin.title('Admin')     
    admin.geometry('500x400')
    admin.configure(bg='darkslategray')
    # Create a Button
    #to write lable
    lbl=Label(admin,text="Welcome admin,")
    lbl.grid(row=1,column=0)
    def CoToStudentControlModule():
        admin.destroy()
        StudentControlModuleScreen()
        
    #first botton
    btn1 = Button(admin, text = 'STUDENTS',  bd = '10', command = CoToStudentControlModule)
    btn1.config(height=2,width=50)
    btn1.grid(row=3,column=1)
    
    def CoToTeacherControlModule():
        admin.destroy()
        TeacherControlModuleScreen()
        
    #second botton
    btn2 = Button(admin, text = 'Teachers', bd = '10', command = CoToTeacherControlModule)
    btn2.grid(row=4,column=1)
    btn2.config(height=2,width=50)
    admin.mainloop()


##gui_basics##
root=Tk()
root.title('login')
w=500
h=300
root.geometry(f'{w}x{h}')
root.configure(bg='darkslategray')

#frame#
frame=Frame(root)
frame['bg']='darkslategray'

#username and entery#
username_lbl=Label(frame,text='Username',bg='darkslategray',fg='white')
username_entry=Entry(frame)
username_lbl.grid(row=0,column=0 ,padx=10,pady=10)
username_entry.grid(row=0,column=1,padx=10,pady=10)

#password and entery#
password_lbl=Label(frame,text='Password',bg='darkslategray',fg='white' )
password_entry=Entry(frame,show='*')
password_lbl.grid(row=1,column=0,padx=10,pady=10)
password_entry.grid(row=1,column=1,padx=10,pady=10)

#combobow###
Pos= StringVar()

combo_lbl=Label(frame,text='Position',bg='darkslategray',fg='white')
objects=['student','admin','teacher']
combo=Combobox(frame,values=objects,state='readonly',width=16,textvariable=Pos)
combo_lbl.grid(row=2,column=0,padx=10,pady=10)
combo.grid(row=2,column=1,padx=10,pady=10)


def action():
    Position=str(Pos.get())
    Email=str(username_entry.get())
    Passowrd=str(password_entry.get())
    
    # To Ensure That Is There Is No Field Is Empty
    if(len(str(Position))==0 or len(Email)==0 or len(Passowrd)==0 ):
        tkinter.messagebox.askokcancel('System','All Data is Required, Please Enter Your Data')
        
    else:
        ### Make Action depending on PositionValue ###
        
        # ADMIN
        if(Position=='admin'):
            
            if(Email=='ADMIN' and Passowrd=='1111'):
                root.destroy()
                AdminScreen()
            else: # Wrong Values
                tkinter.messagebox.showwarning('System','Your Email Or Passowrd is Wrong , Try Again!')
                
        # STUDENT        
        elif(Position=='student'):
        
            flag = Connection_DB.searchStudentPassowrdAndEmail(Passowrd, Email)
            
            if(flag==True):
                #config.studentData = Connection_DB.searchStudentName(Passowrd, Email)
                global StudentData
                StudentData=Connection_DB.searchStudentName(Passowrd, Email)
                root.destroy()
                StudentScreen(StudentData)
            else:
                tkinter.messagebox.askokcancel('System','Your Email Or Passowrd is Wrong , Try Again!')
                
        # TEACHER
        else: # Position == 'teacher'
            
            flag = Connection_DB.searchTeacherPassowrdAndEmail(Passowrd, Email)
            
            if(flag==True):
                teacherClass=Connection_DB.searchTeacherClass(Email, Passowrd)
                root.destroy()
                TeacherScreen(teacherClass)
            else:
                tkinter.messagebox.askokcancel('System','Your Email Or Passowrd is Wrong , Try Again!')
        
    
##login button###
login_btn=Button(frame,text='login',width=7,fg='darkslategray',command=action)
login_btn.grid(row=3,column=1,columnspan=2,padx=1,pady=1)


frame.place(anchor='center',relx=.5,rely=.5)
root.mainloop()

