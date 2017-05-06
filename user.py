#This file will hold the class that will set up the user. It will also form a
#connection to the mongo DB.

#Importing files which will be used in the program
from pymongo import MongoClient
import bcrypt
from bson.son import SON

#The User class is created.
class User():

    def __init__(self, username):
        self.client = MongoClient() #Setting up the connection to mongo DB
        self.db = self.client.user #Creating the user DB
        self.db.users = self.db.users #Creating a users collection within the titanic DB
        self.username = username

    #This method will encrypt the password
    def encrypt_pass(self, password):
        password = password.encode('utf-8')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        return password, hashed

    #This method will add a new member to the database.
    def add(self, username, password):
        self.db.users.insert_one({
            "username": username,
            "password": password
        })

    #This method will find the user within the database
    def find_specific_gt(self, tp):
        bathroom_levels = self.db.paper.find({
            "tp": {"$gt": tp }
        })
        return bathroom_levels

    #This method will see if the user is actual user of the site.
    def check(self, username, password):
        #I first encode the password to utf-8
        password = password.encode('utf-8')
        #I then search for a user that matches the username
        user = self.db.users.find_one({
            "username": username
        });
        #If user is not found then flag is set to False
        if str(user) == 'None':
            flag = False
        #If the user is found, then another check is done to see if the hidden
        #password matches the original one.
        else:
            #Setting the hashed variable to be used in the conditional statement.
            hashed = user['password']
            if bcrypt.hashpw(password, hashed) == hashed:
                #I don't believe I need this user real. I only need to return
                #the flag.
                user_real = self.db.users.find_one({
                    "username": username,
                    "password": password
                });
                flag = True
        return flag
