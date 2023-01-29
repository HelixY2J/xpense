import tkinter as tk
from tkinter import *
import time
from winotify import Notification, audio

import sqlite3


window = tk.Tk()
window.title("Notification test")

frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=3)

frm_form.pack()



lbl_name = tk.Label(master=frm_form, text="Name :")
ent_name = tk.Entry(master=frm_form, width=50)

lbl_name.grid(row=0, column=0, sticky="e")
ent_name.grid(row=0, column=1)


#action function attached to submit button
def action():
    expense = ent_expense.get()
    budget  = ent_bud.get()

    connection = sqlite3.connect("cheapXpsn.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO snow VALUES ("+expense+","+budget+")")
    toast = Notification(  app_id="Ninja script", title="Greetings", msg="Records added",duration="long")
    toast.set_audio(audio.LoopingAlarm4,loop=False)

    toast.show()


    connection.commit()
    connection.close()


#NAME field
lbl_expense = tk.Label(master=frm_form, text="Enter expense :")
ent_expense = tk.Entry(master=frm_form, width=50)

lbl_expense.grid(row=0, column=0, sticky="e")
ent_expense.grid(row=0, column=1)

#BUDGET field
lbl_bud = tk.Label(master=frm_form, text="Whats ur budget:")
ent_bud = tk.Entry(master=frm_form, width=50)

lbl_bud.grid(row=1, column=0, sticky="e")
ent_bud.grid(row=1, column=1)

#buttons portion
frm_buttons = tk.Frame()
frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)


btn_submit = tk.Button(master=frm_buttons, text="Submit",command= action)
btn_submit.pack(side=tk.RIGHT, padx=10, ipadx=10)


btn_clear = tk.Button(master=frm_buttons, text="Clear")
btn_clear.pack(side=tk.RIGHT, ipadx=10)




#user will input it and make a function when exp pass budget then send notif or lif sexpense is 1000 or 100 away from budget 
#set goals for app 
#check others code
# the trigger function should check everytime submit is pressed 

'''connection = sqlite3.connect("cheapXpsn.db")

cursor = connection.cursor()
cursor.execute("CREATE TABLE snow (Expense INTEGER, budget INTEGER)")'''


#cursor.execute("INSERT INTO juan VALUES ('Sammy', 10, 1)")
#ursor.execute("INSERT INTO juan VALUES ('Jamie', 20, 7)")

window.mainloop()