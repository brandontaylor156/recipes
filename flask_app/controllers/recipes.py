from flask_app import app, render_template, request, redirect, session, flash
from flask_app.models import recipe as recipe_module, user as user_module
from datetime import date, datetime

@app.route("/recipe/new")
def recipe_new():
    if 'user_id' not in session:
        return redirect("/")

    return render_template("recipe_add.html")

@app.route("/recipe/insert", methods=['POST'])
def recipe_insert():
    if 'user_id' not in session:
        return redirect("/")

    if not recipe_module.Recipe.validate_recipe(request.form):
        return redirect("/recipe/new")

    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'under': request.form['under'],
        'date_made': request.form['date_made'],
        'user_id': session['user_id']
    }
    new_recipe = recipe_module.Recipe.insert_recipe(data)
    return redirect("/user/dashboard")

@app.route("/recipes/<int:id>")
def view_recipe(id):
    if 'user_id' not in session:
        return redirect("/")

    data = {
        'id': id
    }
    recipe = recipe_module.Recipe.select_recipe_by_id(data)
    print(recipe.name)
    user = user_module.User.select_user_by_recipe_id(data)
    return render_template("recipe_view.html", recipe=recipe, user=user)

@app.route("/recipes/edit/<int:id>")
def recipe_edit(id):
    if 'user_id' not in session:
        return redirect("/")

    data = {
        'id': id
    }
    recipe = recipe_module.Recipe.select_recipe_by_id(data)
    return render_template("recipe_edit.html", recipe=recipe)

@app.route("/recipes/update", methods=['POST'])
def edit_recipe():
    if 'user_id' not in session:
        return redirect("/")

    if not recipe_module.Recipe.validate_recipe(request.form):
        return redirect(f"/recipes/edit/{request.form['id']}")

    data = {
        'id': request.form['id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'under': request.form['under'],
        'date_made': request.form['date_made'],
    }
    recipe_module.Recipe.update_recipe(data)
    return redirect("/user/dashboard")

@app.route("/recipes/delete/<int:id>")
def recipe_delete(id):
    if 'user_id' not in session:
        return redirect("/")
        
    data = {
        'id': id
    }
    recipe_module.Recipe.delete_recipe(data)
    return redirect("/user/dashboard")