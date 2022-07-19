from flask_app import app, render_template, request, redirect, session, flash
from flask_app.models import recipe as recipe_module, user as user_module
from flask_bcrypt import Bcrypt
from pprint import pprint
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user/register", methods=['POST'])
def insert_user():
    if not user_module.User.validate_user(request.form):
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    
    user_id = user_module.User.insert_user(data)
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']
    return redirect("/user/dashboard")

@app.route("/user/dashboard")
def user_dashboard():
    if 'user_id' not in session:
        return redirect("/")

    recipes = recipe_module.Recipe.select_all_recipes()

    users = []
    
    for recipe in recipes:
        data = {
            'id': recipe.user_id
        }
        users.append(user_module.User.select_user_by_user_id(data))

    return render_template("dashboard.html", recipes=recipes, users=users)

@app.route("/user/login", methods=['POST'])
def login_user():
    data = {
        "email": request.form['email'],
    }
    user_in_db = user_module.User.select_user_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password" , 'login')
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", 'login')
        return redirect("/")

    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name

    return redirect("/user/dashboard")

@app.route("/user/logout")
def logout_user():
    session.clear()
    return redirect("/")