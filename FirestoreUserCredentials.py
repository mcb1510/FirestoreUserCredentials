import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

class User:
    
    def __init__(self):
        self.realName = ""
        self.id = 0
        self.birthdate = 0
        self.userName = ""
        self.password = "" 
        self.date = ""
        self.time = ""
        
    def displayInfo(self):
        print(f"Name: {self.realName}") 
        print(f"ID: {self.id}") 
        print(f"Year of Birthdate: {self.birthdate}")    

########################################################################### 
#  This function will get the current date.                               # 
###########################################################################
def getDate():
    
    date = datetime.datetime.now()
    datefinal = f"{date.year}/{date.month}/{date.day}"
    return datefinal

########################################################################### 
#  This function will get the current time.                               # 
###########################################################################
def getTime():
  
    time = datetime.datetime.now()
    timeFinal = f"{time.hour} hours {time.minute} minutes {time.second} seconds."
    return timeFinal

########################################################################### 
# This function will query the users according to their login information.# 
###########################################################################
def admin():
  
    counter = 3
    total = 0
    adminPass = input("Please enter the admin password >> ")
    while adminPass != "CSE310" and counter > 0:        # We only have 3 attempts.
        print(f"Error, {counter} attempts left")
        counter = counter - 1
        adminPass = input("Please enter the admin password >> ")
    if counter == 0:
        print("GET OUT!!!!!!!!!!!!")
        return

    # We choose how to filter users.
    year = (input("Enter year: "))
    month = (input("Enter month: "))
    day = (input("Enter day: "))

    users = db.collection("users").where("date", "==" , f"{year}/{month}/{day}").get()   # We QUERY data according to the date specified.
    print(f"These are the users who have logged in on {year}/{month}/{day} ")
    print()
    for user in users:
        users = user.to_dict()
        print(users["Name"] + " at " + users["time"])
        total = total + 1
    print(f"Total: {total} users.")
    print("See you Boss!")

########################################################################### 
#  This function will change the password of the user.                    # 
###########################################################################
def changePassword(user):
    
    canWe = False
    cPassword = ""
    nPassword = ""
    aPassword = "0"

    while cPassword != user.password:
         cPassword = input("Please enter your current password: ")
         if cPassword != user.password:
             print("Sorry, your answer is wrong. Try again.")
    
    while canWe == False: 
        nPassword = input("Please enter your new password: ")
        aPassword = input("Please enter your new password again: ")
        if nPassword != aPassword:
            print("Sorry, the passwords do not match. Try again.")
        else:
            canWe = True
            db.collection("users").document(user.userName).update({"password": aPassword}) # We MODIFY the data 
            print("You have successfully changed your password.")
            print("You will be redirected to Manage Account Menu")
    
########################################################################### 
#  This function will delete an accout                                    # 
###########################################################################
def deleteAccount(user):
    
    print("You are about to delete your account from the system.")
    print("This will erase all your personal information from our data base.")
    print("Are you sure you want to continue? ")
    answer = input("Yes/No >> ")
    if answer.lower() == "yes":
        db.collection("users").document(user.userName).delete() # We DELETE data  
        print("Your accout has been succesfully deleted.")
        return True
    else:
        print("You will be redirected to Manage Account Menu.")    

########################################################################### 
#  This function will edit an accout                                      # 
###########################################################################
def optionThree():
    
    user = User()
    login(user)
    choice = 0
    while (choice != 3):
      print("")
      print("What do you want to do? ")
      print("1.- Change password")
      print("2.- Delete account")
      print("3.- Go back to Home Menu")
      print()
      choice = int(input("Enter the number option: "))

      if (choice == 1):
        changePassword(user)         #change password 
            
      elif (choice == 2):       #delete your account   
          deleted = deleteAccount(user)
          if deleted == True:
              print("You will be redirected to the Home Menu")
              return

      elif (choice == 3):   # //Exit menu
          print("You will be redirected to the Home Menu.")
          return
      
      else:                           # //  If the user chooses an invalid option
                                       #//  show message.
          print("I am sorry, please choose an available option")

############################################################################### 
#  This function will allow the user to log in into an account. # 
###############################################################################
def optionTwo():

    user = User()
    print()
    print("Perfect!")
    print("Let's log in into your account.\n")
    canWe = login(user)
    if canWe == True:
        print("You have logged in!")
    
########################################################################### 
#  This function will create an account and save it to the data base      # 
###########################################################################
def createAccount(user):
  
    canYou = False
    while (canYou is False):
        print()
        user.userName = input("Enter a username for your profile: ")
        result = db.collection("users").document(user.userName).get()  # to Check if username is in data base already
        
        if result.exists:
            print("Sorry, this username is already been use.")
            print("Try again.")
        else:
            user.password = input("Enter a password: ")
            data = {"Name": user.realName,
                "ID": user.id,
                "Birthdate": user.birthdate,
                "password": user.password,
                "date": user.date}
            db.collection("users").document(user.userName).set(data) # We INSERT data
            canYou = True

            print("Your profile has been successfully created.")
            print("You will be redirected to our home Menu.")   

########################################################################### 
#  This function will prompt the user for his info to create and account. # 
###########################################################################
def optionOne():
    
    user = User()
    answer = ""
    print()
    print("Perfect")
    user.realName = input("Let's create your account. What is your name? ")
    user.id = int(input("Please enter ID number: "))
    user.birthdate = int(input("Please enter your birthdate year: ")) 
    print()
    print("Make sure your personal information is displayed correctly below.")
    print()
    user.displayInfo()

    while (answer != "yes"):
        answer = input("Yes/No ")
        answer = answer.lower()
        if (answer == "yes"):
            createAccount(user)

        elif (answer == "no"):
            print("You will be redirected to our Home Menu.")
            return
        else:
            print("Sorry, I did not understand that. Is your personal information displayed correctly? ")

########################################################################### 
#  This function will check if the credentials are correct. # 
###########################################################################
def login(user):
  
    canWe = False
    while canWe != True:
        username = input("Please enter your Username: ")
        result = db.collection("users").document(username).get()    # We check if the username is in the data base
        if result.exists:                                              
            while canWe != True:
                password = input("Please enter your password: ")
                credentials = result.to_dict()                      # We save the info in a dictionary
                if password == credentials["password"]:
                    user.userName = username
                    user.password = password
                    db.collection("users").document(user.userName).update({"date": getDate()})  # if the password is correct we log in
                    db.collection("users").document(user.userName).update({"time": getTime()})
                    return True                                                                 # and save the time.
                else:
                    print("I am sorry, wrong password")            # wrong password we keep asking
                    print("Try again.")
        else:
            print("I am sorry, we could not find this credential.")
            print("Try again.")      
              
########################################################################### 
#    This function will display and control the Home Page Menu.           # 
###########################################################################
def interact():

    choice = 0
    while (choice != 5):
      print("")
      print("What do you want to do? ")
      print("1.- Sign up")
      print("2.- Log in")
      print("3.- Manage account")
      print("4.- Admin")
      print("5.- Exit")
      choice = int(input("Enter the number option: "))

      if (choice == 1):
        optionOne()         #it is time to create an account
  
      elif (choice == 2):       # log in
        done =  optionTwo()
        if (done):   
         return
            
      elif (choice == 3):       #Edit your account   
          optionThree()

      elif (choice == 4):       #Admin options   
          admin()

      elif (choice == 5):   # //Exit the program
          print("EXIT - We hope to see you soon. BYE!")
      
      else:                           # //  If the user chooses an invalid option
                                       #//  show message.
          print("I am sorry, please choose an available option")
        
#**********************************************************************
# This function will display the Home Page Banner.                    # 
#**********************************************************************
def displayBanner():

    print()
    print("                   Welcome to TeAyudo!")
    print("-------------------------------------------------------------")
    print("     ---------                           --------")
    print("    | SIGN UP |                         | LOG IN |")
    print("     ---------                           --------")
    print(" I don't have an account         I already have an account ")
    print("-------------------------------------------------------------")
#**********************************************************************
# This function is the main function. The program starts here.        #
#**********************************************************************
displayBanner()
interact()
