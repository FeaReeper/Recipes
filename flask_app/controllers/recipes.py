from flask_app import app

from flask_app.models.recipe import Recipe
from flask_app.models.user import User

from flask import render_template, request, redirect, session

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# VIEW ALL RECIPES ROUTE
@app.route("/recipes")
def view_all_recipes():
    data = {
        'id': session['user_id']
    }
    print(session['user_id'])
    return render_template("view_all.html", user = User.get_one(data), recipes = Recipe.get_all())




# CREATE A NEW RECIPE ROUTE
@app.route("/recipes/new")
def create():
    return render_template("new_recipe.html")

# HIDDEN ROUTE TO CREATE THE RECIPE IN DB
@app.route("/recipes/create", methods=['POST'])
def create_recipe():
    under_thirty = request.form['under_thirty']
    if under_thirty == 'True':
        under_thirty = 1
    else:
        under_thirty = 0
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_cooked': request.form['date_cooked'],
        'under_thirty': under_thirty,
        'user_id': session['user_id']
    }
    print(data)
    if not Recipe.validate_recipe(data):
        return redirect('/recipes/new')
    
    Recipe.save(data)
    return redirect("/recipes")


# EDIT RECIPE ROUTE
@app.route("/recipes/<int:id>/edit")
def edit_recipe(id):
    data = {
        'id': id
    }
    return render_template("edit_recipe.html", recipe = Recipe.get_one(data))

# HIDDEN ROUTE TO UPDATE RECIPE
@app.route("/recipes/<int:id>/update", methods = ['POST'])
def update_recipe(id):
    under_thirty = request.form['under_thirty']
    if under_thirty == 'True':
        under_thirty = 1
    else:
        under_thirty = 0

    data = {
        'id': id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_cooked': request.form['date_cooked'],
        'under_thirty': under_thirty
    }
    Recipe.update_recipe(data)
    return redirect("/recipes")


# VIEW ONE RECIPE ROUTE
@app.route("/recipes/<int:id>/view")
def view_one_recipe(id):
    data = {
        'id': id
    }
    data_user = {
        'id': session['user_id']
    }

    return render_template("view_one.html", user = User.get_one(data_user), recipe = Recipe.get_one(data))


# HIDDEN ROUTE TO DELETE ONE RECIPE ROUTE
@app.route('/recipes/<int:id>/delete')
def delete(id):
    Recipe.delete(id)
    return redirect('/recipes')
