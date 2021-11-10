"""
Kenneth Card 

Password Program

10/1/21 - 

This program abides by the password policy created by Kenneth Card - "Password policy.docx"

"""
from os import error
from tkinter import *
from tkinter.messagebox  import showinfo
import string, re, random
import pyperclip

def generate_passwd() :
    """password generator from geekflare shits lit"""
    alphabets = list(string.ascii_letters)
    digits = list(string.digits)
    special_characters = list("!@#$%^&*()")
    characters = list(string.ascii_letters + string.digits + "!@#$%&*")

    ## length of password from the user
    length = random.randint(14,20)

    ## number of character types
    alphabets_count = 1
    digits_count = 2
    special_characters_count = 2

    characters_count = alphabets_count + digits_count + special_characters_count

    ## check the total length with characters sum count
    ## print not valid if the sum is greater than length
    if characters_count > length:
        print("Characters total count is greater than the password length")
        return
    password = []
    ## picking random alphabets
    for i in range(alphabets_count):
        password.append(random.choice(alphabets))
    ## picking random digits
    for i in range(digits_count):
        password.append(random.choice(digits))
    ## picking random alphabets
    for i in range(special_characters_count):
        password.append(random.choice(special_characters))
    ## if the total characters count is less than the password length
    ## add random characters to make it equal to the length
    if characters_count < length:
        random.shuffle(characters)
        for i in range(length - characters_count):
            password.append(random.choice(characters))
    ## shuffling the resultant password
    random.shuffle(password)
    pyperclip.copy("".join(password))
    showinfo("Generated password", "".join(password))


def check_password(pass_value):
    """
    Checks the password for the specified requirements 
    Returns of list of Requirments that passed
    
    """
    
    class Requirement():
        def __init__(self, value, status):
            self.status = status
            self.value = value

    len_pass = len(pass_value)    
    
    symbols = r"[@#$&*?]"
    num = r"\d"
    caps_letter = r"[A-Z]"
    lower_letter= r"[a-z]"
    missing_caps = Requirement('Password is missing a Capital Letter', False)
    missing_lower = Requirement('Password is missing Lowercase letter', False) 
    missing_symbol = Requirement('Password is missing Symbol', False)
    missing_num = Requirement('Password is missing Number', False)
    pass_len  = Requirement('Password Too short Must be >= 14 characters', False)
    
    if len_pass < 14 : 
        pass_len.status = True
    if re.search(caps_letter, pass_value) == None :
        missing_caps.status = True
    if re.search(lower_letter, pass_value) == None :
        missing_lower.status = True
    if re.search(symbols, pass_value) == None :
        missing_symbol.status = True
    if re.search(num, pass_value) == None :
        missing_num.status = True
    passwd_stats = [pass_len, missing_num, missing_caps, missing_lower, missing_symbol]

    return passwd_stats

def get_passwd_input(password_entry) :
    """This function  grabs the password from the GUI User input and parses that information into the proper password class """
    
    fetched_passwd = password_entry.get() #grabs entry
    password_entry.delete(0,END) # clears out entry field
    results_of_check = check_password(fetched_passwd)
    bool_res  = []
    for res in results_of_check :
        bool_res.append(res.status)
    if not any(bool_res):
        showinfo("SUCCESS", "The password entered is acceptable; Good job")
    for requirement in results_of_check :
        if requirement.status :
            showinfo("!!!MISSING REQUIREMENT!!!",requirement.value)

    

def GUI():
    "Creates the GUI and contains the elements of a GUI"
    #window
    tkWindow = Tk()  
    tkWindow.geometry('800x400')  
    tkWindow.title('Password Program')

    #username label and text entry box
    """usernameLabel = Label(tkWindow, text="User Name").grid(row=0, column=0)
    username = StringVar
    usernameEntry = Entry(tkWindow, textvariable=username).grid(row=0, column=1)  """
    
    #password label and password entry box & missing criteria label 
    password_label = Label(tkWindow,text="Password").grid(row=1, column=0)  
    password_entry = Entry(tkWindow, show= '*')
    password_entry.grid(row=1, column=1)
    loginButton = Button(tkWindow, text="Test Password", command=lambda : get_passwd_input(password_entry)).grid(row=4, column=0)
    exitButton = Button(tkWindow, text="Exit Program", command=exit).grid(row=8, column=0)
    password_generator_button = Button(tkWindow, text="Generate a password", command=generate_passwd).grid(row=8, column=4)
    return tkWindow 


def main():
    gui = GUI()
    gui.mainloop()
    return 0
main()




