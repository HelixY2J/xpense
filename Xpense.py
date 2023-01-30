from tkinter import *
from tkinter import messagebox
import sqlite3
import time
import time
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
    gui.configure(bg='#333333')
    Message(gui,font=("Arial", 22, "bold"),bg="#333333", fg="#FFFFFF",text = "NAME      USERNAME      PASSWORD",width=700).pack()
    for row in viewallusers():
        a=row[0]
        b=row[1]
        c=""
        f=len(row[2])
        for i in range (f):
            c= c + "*"
        d = a + "         " + b + "           " + c
        Message(gui,fg='#FFFFFF',font=("Arial", 25, "bold"),bg="#333333",text = d,width=700).pack()
    Button(gui,text="Exit Window", bg="#FF3399", fg="#FFFFFF", font=("Arial", 15),width=10,command=gui.destroy).pack()
    
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
        appwindow()     
    else:
        e1.delete(0,END)
        e2.delete(0,END)
        
        toast = Notification(  app_id="Ninja script", title="Hold on !", msg="Access denied",duration="long")
        toast.set_audio(audio.LoopingAlarm4,loop=False)

        toast.show()

profilename=""
t = 11
# Main window functions
def appwindow():

    def connect1():
        conn=sqlite3.connect("expenseapp.db")
        cur=conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS expensetable(id INTEGER PRIMARY KEY,itemname TEXT,date TEXT,cost TEXT)")
        conn.commit()
        conn.close()
    connect1()

    def insert(itemname,date,cost):
        conn=sqlite3.connect("expenseapp.db")
        cur=conn.cursor()
        cur.execute("INSERT INTO expensetable VALUES(NULL,?,?,?)",(itemname,date,cost))
        conn.commit()
        conn.close()

    def view():
        conn=sqlite3.connect("expenseapp.db")
        cur=conn.cursor()
        cur.execute("SELECT * FROM expensetable")
        rows=cur.fetchall()
        conn.commit()
        conn.close()
        return rows
    
    def search(itemname="",date="",cost=""):
        conn=sqlite3.connect("expenseapp.db")
        cur=conn.cursor()
        cur.execute("SELECT *FROM expensetable WHERE itemname=? OR date=? OR cost=?",(itemname,date,cost))
        rows=cur.fetchall()
        conn.commit()
        conn.close()
        return rows

    def delete(id):
        conn=sqlite3.connect("expenseapp.db")
        cur=conn.cursor()
        cur.execute("DELETE FROM expensetable WHERE id=?",(id))
        conn.commit()
        conn.close()
    
    def deletealldata():
        conn=sqlite3.connect("expenseapp.db")
        cur=conn.cursor()
        cur.execute("DELETE FROM expensetable")
        conn.commit()
        conn.close()
        list1.delete(0,END)
        messagebox.showinfo('Successful', 'All data deleted')

    def sumofitems():
        conn=sqlite3.connect("expenseapp.db")
        cur=conn.cursor()
        cur.execute("SELECT SUM(cost) FROM expensetable")
        sum=cur.fetchone()
        list1.delete(0,END)
        b=str(sum[0])
        a="YOU SPENT " + b
        tost = Notification(  app_id="Ninja script", title="Greetings", msg=a,duration="short")
        tost.set_audio(audio.LoopingAlarm8,loop=False)

        tost.show()
        
        conn.commit()
        conn.close()
        return sum
    
    def check(budget,a,b,c):
        conn=sqlite3.connect("expenseapp.db")
        cur=conn.cursor()
        cur.execute("SELECT SUM(cost) FROM expensetable")
        sum=cur.fetchone()
        list1.delete(0,END)
        exp=str(sum[0])
        
        if exp > budget :
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
        Label(root_2,width=100,height=100,font=("Arial",35),bg="#333333",text="").place(x=-455,y=0)
        Label(root_2,font=("Arial",40),bg="#333333",text="Xpense").place(x=190,y=10)
        Label(root_2,font=("Arial",35),bg="#333333",fg="#FFFFFF",text="(Spend like there is no tomorrow....").place(x=70,y=170)
        Label(root_2,font=("Arial",35),bg="#333333",fg="#FFFFFF",text="And there might not be.....)").place(x=400,y=250)
        Label(root_2,font=("Arial",35),bg="#333333",text="By Group no.9").place(x=500,y=450)
        h=Label(root_2,font=("Arial",35),bg="#333333",text="")
        h.place(x=65,y=650)
        ltime=Label(root_2,font=("century",25),bg="#333333",fg="#FFFFFF")
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

    root_2 = Tk()
    root_2.title("Main page")
    root_2.configure(bg='#333333')
    root_2.geometry("900x700")
    
    #Creating widgets
    l8=Label(root_2,width=60,height=7,font=("Arial",35),bg="#333333",fg="#FFFFFF",text="").place(x=450,y=60)
    l7=Label(root_2,width=100,height=10,font=("Arial",35),bg="#333333",fg="#FFFFFF",text="").place(x=-455,y=410)
    l1=Label(root_2,font=("Arial",17),bg="#333333",fg="#FFFFFF",text="Product name").place(x=10,y=150)
    exp_itemname=StringVar()
    e1=Entry(root_2,font=("Arial",15),textvariable=exp_itemname)
    e1.place(x=220,y=155,height=27,width=165)
    l2=Label(root_2,font=("Arial",17),bg="#333333",fg="#FFFFFF",text="Date(dd-mm-yyyy)").place(x=10,y=200)
    exp_date=StringVar()
    e2=Entry(root_2,font=("Arial",15),textvariable=exp_date)
    e2.place(x=220,y=205,height=27,width=165)
    l3=Label(root_2,font=("Arial",17),bg="#333333",fg="#FFFFFF",text="Cost of product").place(x=10,y=250)
    exp_cost=StringVar()
    e3=Entry(root_2,font=("Arial",15),textvariable=exp_cost)
    e3.place(x=220,y=255,height=27,width=165)
    
    bud=Label(root_2,font=("Arial",17),bg="#333333",fg="#FFFFFF",text="Budget").place(x=600,y=120)
    budget=StringVar()
    b3=Entry(root_2,font=("Arial",15),textvariable=budget)
    b3.place(x=700,y=120,height=27,width=165)
    
    
    
    
    l4=Label(root_2,font=("Arial",17),bg="#333333",fg="#FFFFFF",text="Select ID to delete").place(x=520,y=170)
    exp_id=StringVar()
    sb=Spinbox(root_2, font=("Arial",17),from_= 0, to_ = 200,textvariable=exp_id,justify=CENTER)
    sb.place(x=745,y=174,height=30,width=50)
    scroll_bar=Scrollbar(root_2)
    scroll_bar.place(x=651,y=410,height=277,width=20)  
    list1=Listbox(root_2,height=7,width=30,font=("Arial",20),yscrollcommand = scroll_bar.set)
    list1.place(x=168,y=410)
    scroll_bar.config( command = list1.yview )
    b1=Button(root_2,text="Add Item",font=("Arial",19),bg="#FF3399", fg="#FFFFFF",width=10,command=insertitems).place(x=30,y=300)
    # insert button
    b2=Button(root_2,text="View all items",font=("Arial",19),bg="#FF3399", fg="#FFFFFF",width=12,command=viewallitems).place(x=110,y=355)
    b3=Button(root_2,text="Delete with id",font=("Arial",19),bg="#FF3399", fg="#FFFFFF",width=12,command=deletewithid).place(x=572,y=220)
    b4=Button(root_2,text="Delete all items",font=("Arial",19),bg="#FF3399", fg="#FFFFFF",activeforeground="red",width=15,command=deletealldata).place(x=550,y=280)
    b5=Button(root_2,text="Search",font=("Arial",19),bg="#FF3399", fg="#FFFFFF",width=10,command=search_item).place(x=220,y=298)
    b6=Button(root_2,text="Total spent",font=("Arial",19),bg="#FF3399", fg="#FFFFFF",width=15,command=sumofitems).place(x=550,y=340)
    b7=Button(root_2,text="Close app",font=("Arial",19),bg="#FF3399", fg="#FFFFFF",width=10,command=endpage).place(x=700,y=650)
    
    #is this required , the greeting scetion ?
    name = "Welcome, " + profilename
    l9=Label(root_2,width=60,font=("Arial",30),bg="#333333", fg="#FFFFFF",text=name).place(x=-530,y=61)
    
    root_2.resizable(False, False)
    root_2.mainloop()


# Creating first window for login   
root = Tk()
root.configure(bg='#333333')
#Creating frames
frame = Frame(bd=0, highlightthickness=0, background="#333333").place(relx=0.46, y=0, relwidth=1, relheight=1)
frame2 = Frame(bd=0, highlightthickness=0, background="#333333").place(x=0, rely=0.78, relwidth=1, relheight=1)
root.title("LOGIN / REGISTER")
root.geometry("1000x700")
#Creating widgets in 2 frames
#Style these using custom tkinter

l1=Label(root,font=("Arial",19),bg='#333333',fg="#FFFFFF",text="Username").place(x=80,y=230)
l2=Label(root,font=("Arial",19),bg='#333333',fg="#FFFFFF",text="Password").place(x=80,y=280)
b1=Button(root,text="Login",font=("Arial",19),bg="#FF3399", fg="#FFFFFF",width=12,command=login).place(x=110,y=360)
l6=Label(root,font=("Arial",19),bg='#333333',fg="#FFFFFF",text="Name").place(x=653,y=195)
l3=Label(root,font=("Arial",19),bg='#333333',fg="#FFFFFF",text="Username").place(x=604,y=243)
l4=Label(root,font=("Arial",19),bg='#333333',fg="#FFFFFF",text="Password").place(x=610,y=293)
l5=Label(root,font=("Arial",19),bg='#333333',fg="#FFFFFF",text="Confirm password").place(x=532,y=342)
b2=Button(root,text="Register",font=("Arial",19),bg="#FF3399", fg="#FFFFFF",width=12,command=register).place(x=630,y=400)
login_username=StringVar()
#Placing widgets, no need to change it do we ?
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
Label(root,width=60,font=("Arial",35),bg="#333333",fg="#FF3399",text="Xpense").place(x=-400,y=0)

b3=Button(root,text="Exit Window",font=("Arial",19),bg="#FF3399", fg="#FFFFFF",command=root.destroy).place(x=410,y=630)
b4=Button(root,text="Delete all users",font=("Arial",19),bg="#FF3399", fg="#FFFFFF",width=12,command=deleteallusers).place(x=130,y=620)
b5=Button(root,text="View all users",font=("Arial",19),bg="#FF3399", fg="#FFFFFF",width=12,command=viewwindow).place(x=130,y=560)

root.resizable(False, False)
root.mainloop()
