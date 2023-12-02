# Imports the connection to mySQL database
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User


# Create a class for a dojo to be created
class Recipe:
    DB = "recipes"
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.under_thirty = data['under_thirty']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = None

    @staticmethod
    def validate_recipe(data):
        is_valid = True # we assume this is true
        if len(data['name'].strip()) < 3:
            flash("Name must be at least 3 characters!")
            is_valid = False
        if len(data['description'].strip()) < 3:
            flash("Description must be at least 3 characters!")
            is_valid = False
        if len(data['instructions'].strip()) < 3: 
            flash("Instructions must be at least 3 characters!")
            is_valid = False
        # Still need to change this part of validation
        if data['date_cooked'] == "":
            flash("Date Invalid, Please enter a date!")
            print('Not Working')
            is_valid = False
        if data['under_thirty'] == "":
            flash("Please select if recipe is under 30 minutes!")
            is_valid = False
        return is_valid

# CREATE RECIPE
    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date_cooked, under_thirty, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(under_thirty)s, %(user_id)s);"
        return connectToMySQL(cls.DB).query_db(query, data)
    

# READ RECIPES
    @classmethod
    def get_all(cls):
        # query here needs to join the tables so I can get the recipes where user.id match the id in the route
        query = "SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id;"
        results = connectToMySQL(cls.DB).query_db(query)
        if results:
            recipes = []
            for row in results:
                recipe = cls(row)
                recipe.user_id = User({
                    'id': row['user_id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password']
                })
                recipes.append(recipe)
            return recipes
        

# READ RECIPE
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        if results:
            recipes = []
            for row in results:
                recipe = cls(row)
                recipe.user_id = User({
                    'id': row['user_id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password']
                })
                recipes.append(recipe)
            return recipes[0]

# UPDATE RECIPE
    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_cooked=%(date_cooked)s, under_thirty=%(under_thirty)s WHERE id=%(id)s; "
        return connectToMySQL(cls.DB).query_db(query, data)


# DELETE RECIPE
    @classmethod
    def delete(cls, id):
        query = """DELETE FROM recipes WHERE id = %(id)s;"""
        data = {'id': id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result

