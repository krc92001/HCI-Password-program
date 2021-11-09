import re 
import os
import tkinter


""" 
Password Checking program with GUI and password policy - Kenneth Card

HCI - Professor Chavis
10/24/2021

"""


def GUI():
    """ This will contain the gui and the mainloop for the program
    
    """
    
    pass


def check_passwd(password) :
    """
    Checks the password for the specified requirements
    Returns of list of Requirments that passedd
    """
    
    class Requirement():
        def __init__(self, value, status):
            self.status = status
            self.value = value

    len_pass = len(password)    
    
    symbols = r"[@#$&*]"
    num = r"\d"
    caps_letter = r"[A-Z]"
    lower_letter= r"[a-z]"
    missing_caps = Requirement('missing Capital Letter', False)
    missing_lower = Requirement('missing Lowercase letter', False) 
    missing_symbol = Requirement('missing Symbol', False)
    missing_num = Requirement('missing Number', False)
    pass_len  = Requirement('Password Too short Must be >= 14 characters', False)
    
    if len_pass < 14 : 
        pass_len.status = True
    if re.search(caps_letter, password) == None :
        missing_caps.status = True
    if re.search(lower_letter, password) == None :
        missing_lower.status = True
    if re.search(symbols, password) == None :
        missing_symbol.status = True
    if re.search(num, password) == None :
        missing_num.status = True
    passwd_stats = [pass_len, missing_num, missing_caps, missing_lower, missing_symbol]
    return passwd_stats
        
    """
    This function will check the password for proper criteria using regex
    
    
    """
    
def main() :   
    password = input(" enter a password to check")
    result = check_passwd(password)
    for obj in result :
        if obj.status :
            print(obj.value)
while(True):
    main()
    l = input("exit?")
    if(l == 'y'):
        exit()
