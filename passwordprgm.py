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
import string
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
global login_status
login_status = False
    

"""
This was done because it was the simplest way to make the showinfo boxes print correctly without a nightmare of for loops

"""

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
    if userinput not in list_of_users:
        if  len(userinput) >= 4 :
            newuser = User(userinput,Password("", 1))#new user blank password
        else:
            showinfo("error", "Username must be longer than 3 characters")
            return error
    else :
        showinfo("ERROR", "User account already created with that name")
        return error
    if check_pass(passinput,userinput):
        newuser.passwd.value=passinput
        list_of_users.append(newuser.username)# appends username to list of usernames for password function usage
        user_data.append(newuser) #stores the actual user object for verification
        showinfo("SUCCESS",f"User Account created\nCurrent Users: {list_of_users}")
    else:
        return error

def change_pass(user, newpass):
    global  login_status
    if not login_status :
        showinfo("ERROR", "No user is currently logged in: Please login!\nEnter username, and put the new desired password\nOnce finished click the change password button")
        return error
    user = user.get()
    #for loop  functions similar to SQL statment : SELECT * from USERS where USERNAME = USER_NAME_ENTRY;
    for data in user_data :
        if user == data.username:
            user = data
    
    ##testing 4 iterations of passwords##
    print("List of old passwords: age\n")
    for passw in user.old_passwords :
        print(passw.value + " : "+ str(passw.age))
    ##testing 4 iterations of passwords##
    
    old_passwds=[]
    for oldpass in user.old_passwords :
        old_passwds.append(oldpass.value) #creates list of old passwords

    fetched_password = newpass.get()
    newpasswd = Password(fetched_password, 1)
    if(newpasswd.value == user.passwd.value):
        showinfo("ERROR", "Cannot change password to current password")
        return error
    if(newpasswd.value in old_passwds):
        showinfo("ERROR", "password is in old passwords\ncannot be used until 4 interations have passed")
        return error
    if check_pass(newpasswd.value,user.username) and newpasswd.value not in old_passwds:
        # applys age to passwd if change successful
        for oldpass in user.old_passwords :
            oldpass.age+=1 
            if oldpass.age >= 4 :
                user.old_passwords.remove(oldpass) #removes the passwords that are aged out
        
        #changing user pass obj
        user.old_passwords.append(user.passwd)
        user.passwd=newpasswd
        showinfo("success",f"Changed password to {user.passwd.value}")
        return
    else :
        return error

def show_user_info(username,password):
    "show info of user that is currently logged in"
    
    username = username.get()
    passwd  = password.get()
    for data in user_data:
        if username == data.username and data.passwd.value == passwd:
            encoded_pass = data.passwd.value
            encoded_pass = encoded_pass.encode('utf-8')
            encoded_pass = encoded_pass.hex()
            
            showinfo("UserInfo",f"Username: {data.username}\nPassword= {encoded_pass}")
    pass

def check_from_file(filename):
    """This Function will check a list of passwrods using check_passwd from a file
    
    The format will be 1 password per line
    
    """
    username = None
    if(filename == ''):
        showinfo("ERROR", "NO FILE SELECTED")
        return error
    with open(filename, "r") as input:
        list_of_passwds = input.readlines()
        list_of_results = []
        for passwd in list_of_passwds :
            results = check_password(username, passwd)
            list_of_results.append(results)
    index=0
    for result  in list_of_results :
        
        bool_res  = []
        result_string = ''
        for req in result :
            bool_res.append(req.status)
            #makes  print string
            if(req.status):
                result_string = result_string + req.value + '\n'
        bool_res[5] = False #fixes some poop code
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
    global login_status
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
        for data in user_data:
            if data.username == fetched_username and data.passwd.value ==fetched_passwd:
                showinfo("SUCCESS", f"The User: {fetched_username} login is acceptable; Not sure what you get access to...")
                login_status=True
                cur_user.configure(text = f"Currently logged in as :{fetched_username} {login_status}")
            else: 
                pass
    
    else:
        showinfo("!!!MISSING REQUIREMENT!!!",f"Password: {fetched_passwd}\n{result_string}")

    

def GUI():
    "Creates the GUI and contains the elements of a GUI"
    global login_status
    #GUI only functions - only adjust things pertaining to the gui
    
    def browseFiles():
        filename = filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes = (("Text files","*.txt*"),("all files","*.*")))
        label_file_explorer.configure(text="file selected: "+filename)
        check_from_file(filename)
        label_file_explorer.configure(text= "No file Selected")
    def logout():
        login_status = False
        cur_user_label.configure(text=f"No Current User {login_status}")

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
    
    usernameLabel = Label(tkWindow, image=username_image,highlightthickness=0, background="#75b28b")
    usernameLabel.image = username_image
    usernameLabel.grid(row=0, column=0)
    username_entry = Entry(tkWindow, bg="gray",fg="lightgreen")
    username_entry.grid(row=0, column=1)
    cur_user_label= Label(tkWindow, text="No Current User", background="#75b28b")
    cur_user_label.grid(row=0, column=5)
    
    #password label and password entry box & missing criteria label 
    
    password_label = Label(tkWindow,image=password_label_img, background="#75b28b") 
    password_label.grid(row=1, column=0)
    password_label.image = password_label_img
    
    password_entry = Entry(tkWindow,show= '☺',bg="gray",fg="lightgreen")
    password_entry.grid(row=1, column=1)
    
    #Check from file

    label_file_explorer = Label(tkWindow,text = "  No file Selected   ",fg = "black", background="#75b28b")
    label_file_explorer.grid(row =9,column=0)
    
    button_explore = Button(tkWindow,image=chk_frm_file_img,command = browseFiles,highlightthickness=0,bd=2, bg="black")
    button_explore.image = chk_frm_file_img
    button_explore.grid(row=9,column=1)

    #login for after account is created

    loginButton = Button(tkWindow,borderwidth=.2, highlightthickness=0, image=login_photo, command=lambda : get_passwd_input(username_entry, password_entry, cur_user_label),bd=2, bg="black")
    loginButton.grid(row=1, column=4)
    loginButton.image = login_photo
    logoutButton = Button(tkWindow,image=logout_image, border = 0, highlightthickness=0,command=logout,bd=2, bg="black")
    logoutButton.grid(row=9,column=4)
    logoutButton.image = logout_image
    #Create Users
    
    createUserButton = Button(tkWindow,borderwidth=.2, highlightthickness=0, image=creat_user_img, command=lambda : create_user(username_entry,password_entry),bd=2, bg="black")
    createUserButton.iamge=creat_user_img
    createUserButton.grid(row=0, column=4)

    #Extra function Buttons

    exitButton = Button(tkWindow,image=exit_image,highlightthickness=0,bd=2, bg="black", command=exit)
    exitButton.grid(row=10, column=0)
    exitButton.image=exit_image
    password_generator_button = Button(tkWindow, image=passgen_image, command=generate_passwd, border = 0,highlightthickness=0,bd=2, bg="black")
    password_generator_button.grid(row=10, column=1)
    password_generator_button.image=passgen_image
    change_pass_button = Button(tkWindow,text="Change password",highlightthickness=0, command=lambda: change_pass(username_entry, password_entry),bd=2, bg="#75b28b")
    change_pass_button.grid(row=10,column=4)
    user_info_button = Button(tkWindow, text="show current user info",command=lambda: show_user_info(username_entry,password_entry), bg="#75b28b").grid(row=1,column=5)
    return tkWindow 


def main():
    gui = GUI()
    gui.mainloop()
    return 0
if __name__ == '__main__' :
    main()