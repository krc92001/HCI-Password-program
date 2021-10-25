"""
Kenneth Card 

Password Program

10/1/21

This program abides by the password policy created by Kenneth Card - "Password policy.docx"

"""
from os import error
import tkinter
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




def main():



main()