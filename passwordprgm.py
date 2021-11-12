"""
----------------
Kenneth Card 
----------------
Password Program
----------------
11/14/21 
----------------
This program abides by the password policy created by Kenneth Card - "Password policy.docx"
----------------
"""
from os import error
from tkinter import *
from tkinter.messagebox  import showinfo
from tkinter import filedialog
import string, re, random
from typing import Collection
import pyperclip

#Classes 

class Password():
    def __init__(self, value, age):
        self.value =  value
        self.age = age


class User() :
    def __init__(self, username, passwd):
        self.username = username
        self.passwd = passwd
    old_passwords = []

#User "Database"

global list_of_users # list of usernames - used for checking if username in pass and if username is for an account
global user_data # this holds user objects - associates specific users with passwords
list_of_users = []
user_data = []

def check_pass(pass_value,username) :
    """
    check password for initial  creation
    
    """

    #list of excluded passwords
    excluded_pass_list = ['Password1234!','Password',username]

    class Requirement():
        def __init__(self, value, status):
            self.status = status
            self.value = value
    #regex querys and length of password
    len_pass = len(pass_value)    
    symbols = r"[!@#%$&*?]"
    num = r"\d"
    caps_letter = r"[A-Z]"
    lower_letter= r"[a-z]"

    #requirement objects used for describing missing elements
    missing_caps = Requirement('Password is missing a Capital Letter', False)
    missing_lower = Requirement('Password is missing Lowercase letter', False) 
    missing_symbol = Requirement('Password is missing Symbol', False)
    missing_num = Requirement('Password is missing Number', False)
    pass_len  = Requirement('Password Too short Must be >= 14 characters', False)
    invalid = Requirement('Invalid Password: Username in password or password is in exluded list', False)
    
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
    if(pass_value in excluded_pass_list or username in pass_value) :
        invalid.status = True
    passwd_stats = [pass_len, missing_num, missing_caps, missing_lower, missing_symbol, invalid]
    result_string = '' # used to print errors
    for req in passwd_stats :
        if req.status :
            result_string = result_string+"\n"+req.value
    passwd_status = [pass_len.status, missing_num.status, missing_caps.status, missing_lower.status, missing_symbol.status, invalid.status]
    if not any(passwd_status) :
        return True
    else :
        showinfo("ERROR", f"User Creation invalid bad passwd:\n{result_string}")
        return False


def create_user(username,password):
    userinput = username.get()
    passinput = password.get()
    if userinput not in list_of_users :
        newuser  = User(userinput,Password("", 1))#new user blank password
    else :
        showinfo("ERROR", "User account already created with that name")
        return error
    if check_pass(passinput,userinput):
        newuser.passwd.value=passinput
        list_of_users.append(newuser.username)
        showinfo("SUCCESS",f"User Account created\nCurrent Users: {list_of_users}")
    else:
        return error





def check_from_file(filename):
    """This Function will check a list of passwrods using check_passwd from a file
    
    The format will be 1 password per line
    
    """
    with open(filename, "r") as input:
        list_of_passwds = input.readlines()
        list_of_results = []
        for passwd in list_of_passwds :
            results = check_password(passwd)
            list_of_results.append(results)
    index=0
    for result  in list_of_results :
        
        bool_res  = []
        result_string = ''
        for req in result :
            bool_res.append(req.status)
            if(req.status):
                result_string = result_string + req.value + '\n'
        if not any(bool_res):
            showinfo("SUCCESS", f"The password: {list_of_passwds[index]} is acceptable; Good job")
        
        else:
            showinfo("!!!MISSING REQUIREMENT!!!",f"Password: {list_of_passwds[index]}\n{result_string}")
        index+=1


def generate_passwd() :
    """password generator from geekflare"""
    alphabets = list(string.ascii_letters)
    digits = list(string.digits)
    special_characters = list("!@#$%&*?")
    characters = list(string.ascii_letters + string.digits + "!@#$%&*?")

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
    #random alphabets
    for i in range(alphabets_count):
        password.append(random.choice(alphabets))
    #random digits
    for i in range(digits_count):
        password.append(random.choice(digits))
    #random alphabets
    for i in range(special_characters_count):
        password.append(random.choice(special_characters))
    
    # if the total characters count is less than the password length add random characters to make it equal to the length
    if characters_count < length:
        random.shuffle(characters)
        for i in range(length - characters_count):
            password.append(random.choice(characters))
    ## shuffling the resultant password
    random.shuffle(password)
    pyperclip.copy("".join(password))
    showinfo("Generated password", "Password copied to clipboard: "+"".join(password))


def check_password(username, pass_value):
    """
    Checks the password for the specified requirements 
    Returns of list of Requirments that passed
    
    """

    #list of excluded passwords
    excluded_pass_list = ['Password1234!', ]

    class Requirement():
        def __init__(self, value, status):
            self.status = status
            self.value = value
    #regex querys and length of password
    len_pass = len(pass_value)    
    symbols = r"[!@#%$&*?]"
    num = r"\d"
    caps_letter = r"[A-Z]"
    lower_letter= r"[a-z]"

    #requirement objects used for describing missing elements
    missing_caps = Requirement('Password is missing a Capital Letter', False)
    missing_lower = Requirement('Password is missing Lowercase letter', False) 
    missing_symbol = Requirement('Password is missing Symbol', False)
    missing_num = Requirement('Password is missing Number', False)
    pass_len  = Requirement('Password Too short Must be >= 14 characters', False)
    invalid = Requirement(f'INCORRECT USERNAME RETRY!{username}', False)
    
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
    if(username not in list_of_users) :
        invalid.status = True
    passwd_stats = [pass_len, missing_num, missing_caps, missing_lower, missing_symbol, invalid]

    return passwd_stats

def get_passwd_input(username, password_entry,cur_user) :
    """This function  grabs the password from the GUI User input and parses that information into the proper password class """
    fetched_username = username.get()
    fetched_passwd = password_entry.get() #grabs entry
    username.delete(0,END)
    password_entry.delete(0,END) # clears out entry field
    results_of_check = check_password(fetched_username, fetched_passwd)
    bool_res  = []
    result_string = ''
    for req in results_of_check :
        bool_res.append(req.status)
        if(req.status):
            result_string = result_string + req.value + '\n'
    if not any(bool_res):
        showinfo("SUCCESS", f"The User: {fetched_username} login is acceptable; Not sure what you get access to...")
        cur_user.configure(text = f"Currently logged in as :{fetched_username}")
    
    else:
        showinfo("!!!MISSING REQUIREMENT!!!",f"Password: {fetched_passwd}\n{result_string}")

    

def GUI():
    "Creates the GUI and contains the elements of a GUI"
    #GUI only functions - only adjust things pertaining to the gui
    def browseFiles():
        filename = filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes = (("Text files","*.txt*"),("all files","*.*")))
        label_file_explorer.configure(text="file selected: "+filename)
        check_from_file(filename)
        label_file_explorer.configure(text= "No file Selected")
    def logout():
        cur_user_label.configure(text="No Current User")

    #window init
    tkWindow = Tk()  
    
    #pictures for Graphics
    
    login_photo = PhotoImage(file= r"image_assets\button.png")
    password_label_img = PhotoImage(file= r"image_assets\password.png")
    background_image = PhotoImage(file=r"image_assets\Cool_Backgrounds.png")
    logout_image = PhotoImage(file= r"image_assets\logout.png")
    exit_image = PhotoImage(file= r"image_assets\exit.png")
    username_image = PhotoImage(file= r"image_assets\username.png")
    creat_user_img = PhotoImage(file= r"image_assets\createuser.png")
    passgen_image = PhotoImage(file=r"image_assets\passgen.png")
    chk_frm_file_img = PhotoImage(file=r"image_assets\checkfromfile.png")
    #window settings
    tkWindow.resizable(False,False)
    tkWindow.title("Password Program - Kenny Card")
    tkWindow.geometry('800x400')
    tkWindow.config(background="white")
    background_label = Label(tkWindow, image=background_image)
    background_label.image=background_image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    tkWindow.wm_attributes("-transparentcolor", "orange")
    
    #username label and text entry box
    
    usernameLabel = Label(tkWindow, image=username_image,highlightthickness=0,bd=0)
    usernameLabel.image = username_image
    usernameLabel.grid(row=0, column=0)
    username_entry = Entry(tkWindow, bg="gray",fg="lightgreen")
    username_entry.grid(row=0, column=1)
    cur_user_label= Label(tkWindow, text="No Current User", background="#75b28b")
    cur_user_label.grid(row=0, column=5)
    
    #password label and password entry box & missing criteria label 
    
    password_label = Label(tkWindow,image=password_label_img,bg = "#75b28b", border = 1) 
    password_label.grid(row=1, column=0)
    password_label.image = password_label_img
    
    password_entry = Entry(tkWindow,show= '☺',bg="gray",fg="lightgreen")
    password_entry.grid(row=1, column=1)
    
    #Check from file

    label_file_explorer = Label(tkWindow,text = "  No file Selected   ",fg = "black", background="#75b28b")
    label_file_explorer.grid(row =9,column=0)
    
    button_explore = Button(tkWindow,image=chk_frm_file_img,command = browseFiles, border = 0,highlightthickness=0)
    button_explore.image = chk_frm_file_img
    button_explore.grid(row=9,column=1)

    #login for after account is created

    loginButton = Button(tkWindow,borderwidth=.2, highlightthickness=0, image=login_photo, command=lambda : get_passwd_input(username_entry, password_entry, cur_user_label))
    loginButton.grid(row=1, column=4)
    loginButton.image = login_photo
    logoutButton = Button(tkWindow,image=logout_image, border = 0, highlightthickness=0,command=logout)
    logoutButton.grid(row=9,column=4)
    logoutButton.image = logout_image
    #Create Users
    
    createUserButton = Button(tkWindow,borderwidth=.2, highlightthickness=0, image=creat_user_img, command=lambda : create_user(username_entry,password_entry))
    createUserButton.iamge=creat_user_img
    createUserButton.grid(row=0, column=4)

    #Extra function Buttons

    exitButton = Button(tkWindow,image=exit_image,highlightthickness=0,bd=0, command=exit, border = 0)
    exitButton.grid(row=10, column=0)
    exitButton.image=exit_image
    password_generator_button = Button(tkWindow, image=passgen_image, command=generate_passwd, border = 0,highlightthickness=0)
    password_generator_button.grid(row=10, column=1)
    password_generator_button.image=passgen_image
    return tkWindow 


def main():
    gui = GUI()
    gui.mainloop()
    return 0

main()