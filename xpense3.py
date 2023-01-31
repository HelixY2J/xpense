from tkinter import *
from tkinter import messagebox
import sqlite3
import time
import time
import numpy as np
import customtkinter
import matplotlib.pyplot as plt
from winotify import Notification, audio

# cant decide where to use that counter function
# budget < exp yet to implement line 194
# Use custom tkinter



#Defining functions 
def connect():
    conn=sqlite3.connect("loginpage.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT,username TEXT,password TEXT)")
    conn.commit()
    conn.close()
connect()

def viewallusers():
    conn=sqlite3.connect("loginpage.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM users")
    rows=cur.fetchall()
    conn.commit()
    conn.close()   
    return rows

def adduser(name,username,password):
    conn=sqlite3.connect("loginpage.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO users VALUES(?,?,?)",(name,username,password))
    conn.commit()
    conn.close()

def deleteallusers():
    conn=sqlite3.connect("loginpage.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM users")
    conn.commit()
    conn.close()
    messagebox.showinfo('Successful', 'All users deleted')

def checkuser(username,password):
    conn=sqlite3.connect("loginpage.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))
    result=cur.fetchone()
    return result

def getusername(username,password):
    conn=sqlite3.connect("loginpage.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))
    result=cur.fetchone()
    global profilename
    if result!=None:
        profilename=result[0]

def viewwindow():
    gui = Toplevel(root)
    gui.title("VIEW ALL USERS")
    gui.geometry("800x700")
    gui.configure(bg='#2C2C2C')
    Message(gui,font=("Arial", 22, "bold"),bg="#2C2C2C", fg="#00D1FF",text = "NAME      USERNAME      PASSWORD",width=700).pack()
    for row in viewallusers():
        a=row[0]
        b=row[1]
        c=""
        f=len(row[2])
        for i in range (f):
            c= c + "*"
        d = a + "         " + b + "           " + c
        Message(gui,fg='#75E0F8',font=("Arial", 25, "bold"),bg="#2C2C2C",text = d,width=700).pack()
    b=customtkinter.CTkButton(gui,text="Exit Window", bg_color="#00D1FF",fg_color="#00D1FF", text_color="#01333E",hover_color="#1785A8",corner_radius=0,border_width=0,border_spacing=0,border_color="#00D1FF", font=("Arial", 15),width=10,command=gui.destroy).pack()
    
def register():
    a = register_name.get()
    b = register_username.get()
    c = register_password.get()
    d = register_repassword.get()
    if c==d and c!="" and len(c)>2 and a!="" and b!="":
        adduser(a,b,c)
        messagebox.showinfo(':)', 'Registration Successful')      
    else :
        if(a=="" or b=="" or c=="" or d==""):
            messagebox.showinfo('oops something wrong', 'Field should not be empty')
        else:
            messagebox.showinfo('oops something wrong', 'Passwords dont match,Try again Or\nPassword should contain atleast 3 characters')
            '''pass_regis = Notification(  app_id="Ninja script", title="Hold on !", msg="Passwords dont match,Try again \nPassword should contain atleast 6 characters",duration="long")
            pass_regis.set_audio(audio.LoopingAlarm4,loop=False)
            pass_regis.show()'''
    e3.delete(0,END)
    e4.delete(0,END)
    e5.delete(0,END)
    e6.delete(0,END)

def login():
    a = login_username.get()
    b = login_password.get()
    getusername(a,b)   
    if (checkuser(a,b))!=None:
        root.destroy()
        appwindow(a)
    else:
        e1.delete(0,END)
        e2.delete(0,END)
        
        toast = Notification(  app_id="Ninja script", title="Hold on !", msg="Access denied",duration="short")
        toast.set_audio(audio.LoopingAlarm4,loop=False)

        toast.show()

profilename=""
t = 11
# Main window functions
def appwindow(username):
    def connect1():
        conn = sqlite3.connect("expenseapp.db")
        cur = conn.cursor()
        cur.execute(f"CREATE TABLE IF NOT EXISTS {username}(id INTEGER PRIMARY KEY,itemname TEXT,date TEXT,cost TEXT)")
        conn.commit()
        conn.close()

    connect1()

    def insert(itemname, date, cost):
        conn = sqlite3.connect("expenseapp.db")
        cur = conn.cursor()
        cur.execute(f"INSERT INTO {username} VALUES(NULL,?,?,?)", (itemname, date, cost))
        conn.commit()
        conn.close()

    def view():
        conn = sqlite3.connect("expenseapp.db")
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {username}")
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        return rows

    def search(itemname="", date="", cost=""):
        conn = sqlite3.connect("expenseapp.db")
        cur = conn.cursor()
        cur.execute(f"SELECT *FROM {username} WHERE itemname=? OR date=? OR cost=?", (itemname, date, cost))
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        return rows

    def delete(id):
        conn = sqlite3.connect("expenseapp.db")
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {username} WHERE id=?", (id))
        conn.commit()
        conn.close()

    def deletealldata():
        conn = sqlite3.connect("expenseapp.db")
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {username}")
        conn.commit()
        conn.close()
        list1.delete(0, END)
        messagebox.showinfo('Successful', 'All data deleted')

    def sumofitems():
        conn = sqlite3.connect("expenseapp.db")
        cur = conn.cursor()
        cur.execute(f"SELECT SUM(cost) FROM {username}")
        sum = cur.fetchone()
        list1.delete(0, END)
        b = str(sum[0])
        a = "You have spent " + b
        tost = Notification(app_id="Ninja script", title="Greetings", msg=a, duration="short")
        tost.set_audio(audio.LoopingAlarm10, loop=False)

        tost.show()

        conn.commit()
        conn.close()
        return sum
    
    def graph():
        conn=sqlite3.connect('expenseapp.db')
        cur=conn.cursor()
        plt.figure()
        ax1=plt.subplot(1, 1, 1)

        
        cur.execute(f"SELECT itemname, cost FROM {username}")
        item=[]
        sizes=[]
        for row in cur.fetchall(): 
        
         item.append(row[0])
         sizes.append(row[1])
         
        box = np.zeros(len(sizes))
        maxpos= sizes.index(max(sizes))
        box[maxpos]= 0.07
        print(sizes)
        print(box)
         
        ax1.pie(sizes, explode=box,  labels=item, autopct='%1.1f%%',
        shadow=True, startangle=90)
        ax1.axis('equal')

        plt.plot()
        plt.show()

    def check(budget, a, b, c):
        conn = sqlite3.connect("expenseapp.db")
        cur = conn.cursor()
        cur.execute(f"SELECT SUM(cost) FROM {username}")
        sum = cur.fetchone()
        list1.delete(0, END)
        exp = int(sum[0])
        #exp = int(exp)
        budget = int(budget)
        if exp > budget :
           # messagebox.showinfo('Successful', 'All data deleted')
            up = Notification(  app_id="Ninja script", title="Uh-oh", msg="You crossed ur budget",duration="short")
            up.set_audio(audio.LoopingAlarm8,loop=False)

            up.show()
             
        else:
            insert(a,b,c)
            e1.delete(0,END)
            e2.delete(0,END)
            e3.delete(0,END)
        list1.delete(0,END)
            
            
        
    
    def insertitems():
        a=exp_itemname.get()
        b=exp_date.get()
        c=exp_cost.get()
        f = budget.get()
        
        d=c.replace('.', '', 1)
        e=b.count('-')      

        if a=="" or b=="" or c=="":
            messagebox.showinfo("oops!","Field should not be empty")
        elif len(b)!=10 or e!=2:
            messagebox.showinfo("oops!","DATE should be in format dd-mm-yyyy")
        elif (d.isdigit()==False):
            messagebox.showinfo("Cost should be a number")
        else:
            check(f,a,b,c)
            
            '''insert(a,b,c)
            e1.delete(0,END)
            e2.delete(0,END)
            e3.delete(0,END)
        list1.delete(0,END)'''

    def viewallitems():
        list1.delete(0,END)
        list1.insert(END,"ID   NAME     DATE      COST")
        for row in view():
            a=str(row[0])
            b=str(row[1])
            c=str(row[2])
            d=str(row[3])
            f= a + "     " + b + "    " + c + "    " + d
            list1.insert(END,f)
    
    def deletewithid():
        list1.delete(0,END)
        a=exp_id.get()
        delete(a)
    
    def search_item():
        list1.delete(0,END)
        list1.insert(END,"ID   NAME     DATE      COST")
        for row in search(exp_itemname.get(),exp_date.get(),exp_cost.get()):
            a=str(row[0])
            b=str(row[1])
            c=str(row[2])
            d=str(row[3])
            f= a + "     " + b + "    " + c + "    " + d
            list1.insert(END,f)
        e1.delete(0,END)
        e2.delete(0,END)
        e3.delete(0,END)
    
    def endpage():
        Label(root_2,width=100,height=100,font=("Arial",35),bg="#2C2C2C",text="").place(x=-455,y=0)
        Label(root_2,font=("Arial",40),bg="#2C2C2C",text="Xpense").place(x=190,y=10)
        Label(root_2,font=("Arial",35),bg="#2C2C2C",fg="#FFFFFF",text="(Spend like there is no tomorrow....").place(x=70,y=170)
        Label(root_2,font=("Arial",35),bg="#2C2C2C",fg="#FFFFFF",text="And there might not be.....)").place(x=400,y=250)
        Label(root_2,font=("Arial",35),bg="#2C2C2C",text="By Group no.9").place(x=500,y=450)
        h=Label(root_2,font=("Arial",35),bg="#2C2C2C",text="")
        h.place(x=65,y=650)
        ltime=Label(root_2,font=("century",25),bg="#2C2C2C",fg="#FFFFFF")
        ltime.place(x=655,y=651)      
        def timer():
            global t
            a=str(t)+" seconds"
            text_input = a
            ltime.config(text=text_input)
            ltime.after(1000, timer)
            t=t-1
        timer()
        root_2.after(11000,root_2.destroy)


#Creating 2nd window for main page

    root_2 = customtkinter.CTk()
    root_2.title("Main page")
    root_2.configure(bg='#2C2C2C')
    # root_2.configure(fg_color="pink")
    root_2.geometry("800x700")
    
    #Creating widgets
    l8=Label(root_2,width=60,height=7,font=("Arial",35),bg="#2C2C2C",fg="#FFFFFF",text="").place(x=450,y=60)
    l7=Label(root_2,width=100,height=10,font=("Arial",35),bg="#2C2C2C",fg="#FFFFFF",text="").place(x=-455,y=410)
    l1=customtkinter.CTkLabel(root_2,font=("Arial",17),bg_color="#242424",text_color="#00D1FF",text="Product name").place(x=10,y=120)
    exp_itemname=StringVar()
    e1=Entry(root_2,font=("Arial",15),textvariable=exp_itemname)
    e1.place(x=220,y=155,height=27,width=165)
    l2=customtkinter.CTkLabel(root_2,font=("Arial",17),bg_color="#242424",text_color="#00D1FF",text="Date(dd-mm-yyyy)").place(x=10,y=160)
    exp_date=StringVar()
    e2=Entry(root_2,font=("Arial",15),textvariable=exp_date)
    e2.place(x=220,y=205,height=27,width=165)
    l3=customtkinter.CTkLabel(root_2,font=("Arial",17),bg_color="#242424",text_color="#00D1FF",text="Cost of product").place(x=10,y=200)
    exp_cost=StringVar()
    e3=Entry(root_2,font=("Arial",15),textvariable=exp_cost)
    e3.place(x=220,y=255,height=27,width=165)
    
    bud=customtkinter.CTkLabel(root_2,font=("Arial",17),bg_color="#2C2C2C",text_color="#00D1FF",text="Budget").place(x=500,y=90)
    budget=StringVar()
    b3=Entry(root_2,font=("Arial",15),textvariable=budget)
    b3.place(x=700,y=120,height=27,width=165)
    
    b4=customtkinter.CTkButton(root_2,text="Graph my expense", fg_color="#00D1FF",font=("Arial",19), text_color="#01333E",hover_color="#1785A8",corner_radius=0,border_width=0,border_spacing=0,border_color="#0097C7",width=150,command= graph).place(x=550,y=60)
    
    
    l4=customtkinter.CTkLabel(root_2,font=("Arial",17),bg_color="#2C2C2C",text_color="#00D1FF",text="Select ID to delete").place(x=455,y=135)
    exp_id=StringVar()
    sb=Spinbox(root_2, font=("Arial",17),from_= 0, to_ = 200,textvariable=exp_id,justify=CENTER)
    sb.place(x=745,y=174,height=30,width=50)
    scroll_bar=Scrollbar(root_2)
    scroll_bar.place(x=651,y=440,height=240,width=20)  
    list1=Listbox(root_2,height=7,width=30,bg="black",fg="white",font=("Arial",20),yscrollcommand = scroll_bar.set)
    list1.place(x=168,y=440)
    scroll_bar.config( command = list1.yview )
    b1=customtkinter.CTkButton(root_2,text="Add Item",font=("Arial",19),bg_color="#00D1FF",fg_color="#00D1FF", text_color="#01333E",hover_color="#1785A8",corner_radius=0,border_width=0,border_spacing=0,border_color="#00D1FF",width=100,command=insertitems).place(x=70,y=250)
    # insert button
    b2=customtkinter.CTkButton(root_2,text="View all items",font=("Arial",19),bg_color="#00D1FF",fg_color="#00D1FF", text_color="#01333E",hover_color="#1785A8",corner_radius=0,border_width=0,border_spacing=0,border_color="#00D1FF",width=100,command=viewallitems).place(x=110,y=290)
    b3=customtkinter.CTkButton(root_2,text="Delete with id",font=("Arial",19),bg_color="#00D1FF",fg_color="#00D1FF", text_color="#01333E",hover_color="#1785A8",corner_radius=0,border_width=0,border_spacing=0,border_color="#00D1FF",width=150,command=deletewithid).place(x=510,y=180)
    b4=customtkinter.CTkButton(root_2,text="Delete all items",font=("Arial",19),bg_color="#00D1FF",fg_color="#00D1FF", text_color="#01333E",hover_color="#1785A8",corner_radius=0,border_width=0,border_spacing=0,border_color="#00D1FF",width=150,command=deletealldata).place(x=510,y=230)
    b5=customtkinter.CTkButton(root_2,text="Search",font=("Arial",19),bg_color="#00D1FF",fg_color="#00D1FF", text_color="#01333E",hover_color="#1785A8",corner_radius=0,border_width=0,border_spacing=0,border_color="#00D1FF",width=100,command=search_item).place(x=190,y=250)
    b6=customtkinter.CTkButton(root_2,text="Total spent",font=("Arial",19),bg_color="#00D1FF",fg_color="#00D1FF", text_color="#01333E",hover_color="#1785A8",corner_radius=0,border_width=0,border_spacing=0,border_color="#00D1FF",width=150,command=sumofitems).place(x=510,y=280)
    b7=customtkinter.CTkButton(root_2,text="Close app",font=("Arial",19),bg_color="#00D1FF",fg_color="#00D1FF", text_color="#01333E",hover_color="#1785A8",corner_radius=0,border_width=0,border_spacing=0,border_color="#00D1FF",width=150,command=endpage).place(x=510,y=570)
    
    #is this required , the greeting scetion ?
    name = "Welcome, " + profilename
    l9=customtkinter.CTkLabel(root_2,width=60,font=("Arial",30,"bold"),bg_color="#242424", text_color="#59E1FF",text="  "+name).place(x=0,y=61)
    
    root_2.resizable(False, False)
    root_2.mainloop()


# Creating first window for login   
root = customtkinter.CTk()
root.configure(bg='#2C2C2C')
#Creating frames
frame = customtkinter.CTkFrame(root,border_width=0, bg_color="#2C2C2C").place(relx=0.5, y=0, relwidth=1, relheight=1)
frame2 = customtkinter.CTkFrame(root,border_width=0, bg_color="#2C2C2C").place(x=0, rely=0.8, relwidth=1, relheight=1)
root.title("LOGIN / REGISTER")
root.geometry("800x700")
#Creating widgets in 2 frames
#Style these using custom tkinter

l1=customtkinter.CTkLabel(root,font=("Arial",18),bg_color='#242424',text="Username",text_color="#00D1FF").place(x=80,y=185)
l2=customtkinter.CTkLabel(root,font=("Arial",18),bg_color='#242424',text="Password",text_color="#00D1FF").place(x=80,y=225)
b1=customtkinter.CTkButton(root,text="Login",font=("Arial",19),bg_color="#00D1FF", fg_color="#00D1FF",text_color="#01333E",corner_radius=0,border_width=0,border_spacing=0,border_color="#00D1FF",hover_color="#1785A8",width=120,command=login).place(x=130,y=280)
l6=customtkinter.CTkLabel(root,font=("Arial",18),bg_color='#2C2C2C',text_color="#00D1FF",text="Name").place(x=535,y=158)
l3=customtkinter.CTkLabel(root,font=("Arial",18),bg_color='#2C2C2C',text_color="#00D1FF",text="Username").place(x=500,y=195)
l4=customtkinter.CTkLabel(root,font=("Arial",18),bg_color='#2C2C2C',text_color="#00D1FF",text="Password").place(x=500,y=235)
l5=customtkinter.CTkLabel(root,font=("Arial",18),bg_color='#2C2C2C',text_color="#00D1FF",text="Confirm password").place(x=445,y=275)
b2=customtkinter.CTkButton(root,text="Register",font=("Arial",19),bg_color="#00D1FF", fg_color="#00D1FF",text_color="#01333E",corner_radius=0,border_width=0,border_spacing=0,border_color="#00D1FF",hover_color="#1785A8",width=120,command=register).place(x=540,y=330)
login_username=StringVar()


#Placing widgets, no need to change it do we ?  ........i will try if i can do something with borders
e1=Entry(root,font=("adobe clean",15),textvariable=login_username)
e1.place(x=205,y=238,height=25,width=165)
login_password=StringVar()
e2=Entry(root,font=("adobe clean",15),textvariable=login_password,show="*")
e2.place(x=205,y=287,height=25,width=165)
register_name=StringVar()
e6=Entry(root,font=("adobe clean",15),textvariable=register_name)
e6.place(x=740,y=200,height=25,width=165)
register_username=StringVar()
e3=Entry(root,font=("adobe clean",15),textvariable=register_username)
e3.place(x=740,y=250,height=25,width=165)
register_password=StringVar()
e4=Entry(root,font=("adobe clean",15),textvariable=register_password, show="*")
e4.place(x=740,y=300,height=25,width=165)
register_repassword=StringVar()
e5=Entry(root,font=("adobe clean",15),textvariable=register_repassword, show="*")
e5.place(x=740,y=350,height=25,width=165)


#The 3rd frame , style these accordingly
Label(root,width=60,font=("Arial",35,"bold"),bg="#2C2C2C",fg="#00D1FF",text="Xpense").place(x=-370,y=0)

b3=customtkinter.CTkButton(root,text="Exit Window",font=("Arial",19),bg_color="#00D1FF",fg_color="#00D1FF", text_color="#01333E",hover_color="#1785A8",corner_radius=0,border_width=0,border_spacing=0,border_color="#00D1FF",command=root.destroy).place(x=350,y=600)
b4=customtkinter.CTkButton(root,text="Delete all users",font=("Arial",19),bg_color="#00D1FF",fg_color="#00D1FF", text_color="#01333E",hover_color="#1785A8",corner_radius=0,border_width=0,border_spacing=0,border_color="#00D1FF",command=deleteallusers).place(x=120,y=460)
b5=customtkinter.CTkButton(root,text="View all users",font=("Arial",19),bg_color="#00D1FF",fg_color="#00D1FF", text_color="#01333E",hover_color="#1785A8",corner_radius=0,border_width=0,border_spacing=0,border_color="#00D1FF",command=viewwindow).place(x=120,y=410)

root.resizable(False, False)
root.mainloop()