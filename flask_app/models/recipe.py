from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app, flash, session
from pprint import pprint
from datetime import date, datetime

DATABASE = 'recipes_schema'

class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.under = data['under']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def select_recipe_by_id(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return Recipe(results[0]) 

    @classmethod
    def select_all_recipes(cls):
        query = "SELECT * FROM recipes ORDER BY name;"
        results = connectToMySQL(DATABASE).query_db(query)
        recipes = []
        for result in results:
            recipes.append( Recipe(result) )
        return recipes 

    @classmethod
    def insert_recipe(cls, data):
        query = "INSERT INTO recipes (name, under, description, instructions, user_id, date_made) VALUES (%(name)s, %(under)s, %(description)s, %(instructions)s, %(user_id)s, %(date_made)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under = %(under)s, date_made = %(date_made)s WHERE recipes.id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE recipes.id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return  

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True

        if len(recipe['name']) < 3:
            flash("Name must be at least 3 characters long.", 'name')
            is_valid = False

        if len(recipe['description']) < 3:
            flash("Description must be at least 3 characters long.", 'description')
            is_valid = False

        if len(recipe['instructions']) < 3:
            flash("Instructions must be at least 3 characters long.", 'instructions')
            is_valid = False

        if recipe['date_made'] == "":
            flash("Date required", 'date_made')
            is_valid = False
            return is_valid
        if (datetime.strptime(recipe['date_made'], '%Y-%m-%d').date()) > date.today():
            flash("Date invalid.", 'date_made')
            is_valid = False

        return is_valid
