# Imports the connection to mySQL database
from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash
import re	# the regex module

# Create a class for a dojo to be created
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    DB = "recipes"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        # self.created_at = data['created_at']
        # self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(data):
        is_valid = True # we assume this is true
        if len(data['first_name'].strip()) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(data['last_name'].strip()) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(data['password'].strip()) < 8:
            flash("Password must be at least 8 characters!")
            is_valid = False
        if not data['password'] == data['confirm']:
            is_valid = False
        return is_valid

# CREATE
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.DB).query_db(query, data)


# READ
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        return cls(result[0])

    




    # @staticmethod
    # def validate_user(user):
    #     is_valid = True
    #     # test whether a field matches the pattern
    #     if not EMAIL_REGEX.match(user['email']): 
    #         flash("Invalid email address!")
    #     is_valid = False
    #     return is_valid


