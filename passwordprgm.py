"""
Kenneth Card 

Password Program

10/1/21 - 

This program abides by the password policy created by Kenneth Card - "Password policy.docx"

"""
from os import error
from tkinter import *
import re
from getpass import getpass

class password:
    value = ""
    age = 1
    def check_password():
        """Checks the validity of passwords"""
        

class User:
    cur_password = "password" #default password is password
    old_passwords = [] # stores previous passwords for 4 iterations
    def __init__(self, name):
        "assigns a username to each unique user created"
        self.username = name
    
    
    def create_passwd(cur_password,  old_passwords):
        """allows user to create a password"""
        old_passwords.append(cur_password)
        user_pass = password()
        user_pass.value = getpass("Enter a password: ")
        cur_password = user_pass

def create_user(username, Current_users):
    """This just creates a user; returns a user object"""
    if username in Current_users:
        print("error user already exists")
        return error
    new_user = User(username)
    Current_users.append(new_user.username)
    return new_user
def test_login(password) :
    if password != None :
        print("This worked")
        return True

def GUI():
    "Creates the GUI and contains the elements of a GUI"
    #window
    tkWindow = Tk()  
    tkWindow.geometry('400x150')  
    tkWindow.title('Tkinter Login Form - pythonexamples.org')

    #username label and text entry box
    """usernameLabel = Label(tkWindow, text="User Name").grid(row=0, column=0)
    username = StringVar
    usernameEntry = Entry(tkWindow, textvariable=username).grid(row=0, column=1)  """

    #password label and password entry box
    passwordLabel = Label(tkWindow,text="Password").grid(row=1, column=0)  
    password = StringVar()
    passwordEntry = Entry(tkWindow, textvariable=password, show='*').grid(row=1, column=1)
    loginButton = Button(tkWindow, text="Login", command=lambda :test_login(password)).grid(row=4, column=0)
    return tkWindow 


def main():
    gui = GUI()
    gui.mainloop()
    return 0
main()