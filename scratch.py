import mysql.connector as mysql
import requests
from flask import Flask, request, render_template, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_session import Session
from datetime import datetime, timedelta

app = Flask(__name__)

# Secret key for session management
app.secret_key = '123AMM'

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Example: session lasts for 7 days
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure session cookies are only sent over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to session cookies

#API key
api_key = "653ac8f884cb4c99bdd950abd9d769c9"

HOST = "igor.gold.ac.uk"
DATABASE = "avidl002_Project"
USER = "avidl002"
PASSWORD = "asdf"
PORT = 3307

db = mysql.connect(
    host=HOST,
    database=DATABASE,
    user=USER,
    password=PASSWORD,
    port=PORT
)

login_manager = LoginManager(app)

Session(app)

# Define a simple User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

@login_manager.user_loader
def load_user(email):
    # Load user from database by name (treated as if it were the id)
    print("Loading user:", email)
    cursor = db.cursor()
    cursor.execute("SELECT name, email FROM Users WHERE email = %s", (email,))
    user_data = cursor.fetchone()
    if user_data:
        user = User(name=user_data[0], email=user_data[1])
        print("User loaded:", user)  # Add this line for debuggings
        return user
    else:
        print("User not found") 
        return None

@app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return render_template('index.html')
    elif request.method == 'GET':
        return render_template('index.html')

@app.route('/find_recipe', methods=['POST'])
@login_required
def process_form():
    user_input = request.form['user_input']
    print('User Input:', user_input)


    # Endpoint URL
    endpoint = 'https://api.spoonacular.com/recipes/complexSearch'


    #  Search paramerters
    params = {
        'apiKey': api_key,
        'query': user_input, # User written imput (natural language)
    }

    # GET request
    response = requests.get(endpoint, params=params)

    # Check if request was successful 
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()

        results = []

        # Print data recipe titles
        for result in data['results']:
            results.append(result)
        
        # Return webpage
        return render_template('find_recipe.html', results=results)

    else:
        print('Error: ', response.status_code)

@app.route('/recipe', methods=['GET'])
@login_required
def recipe():
    # Get recipe id from URL parameter
    recipeId = request.args.get('id')

    # Endpoint URL
    endpoint = "https://api.spoonacular.com/recipes/{0}/information".format(recipeId)

    #  Search paramerters
    params = {
        'apiKey': api_key,
    }

    # GET request
    response = requests.get(endpoint, params=params)

    # Check if request was successful 
    if response.status_code == 200:
        # Parse JSON response
        recipe = response.json()

        # Return webpage
        return render_template('recipe.html', recipe=recipe)

    else:
        print('Error: ', response.status_code)

# User sign up 
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    print('route accessed')
    if request.method == 'POST':
        print('form submitted')
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        print(f"Form data: name={name}, email={email}, password={password}, confirm_password={confirm_password}")

        if password == confirm_password:
            print('Passwords match')
            cursor = db.cursor()
            try:
                # Check if user already exists (email)
                cursor.execute("SELECT * FROM Users WHERE LOWER(email) = LOWER(%s)", (email,))
                existing_user = cursor.fetchone()

                if existing_user:
                    # If user already exists, compare passwords
                    # login_message = "User with this email already exists. Would you like to <a href='/login'>login</a>?"
                    # return login_message
                    print('User Exists')
                    return render_template('signup.html', error="User with this email already exists. Would you like to <a href='/login'>login</a>?")

                else:
                    hashed_password = generate_password_hash(password).decode('utf-8')
                    cursor.execute("INSERT INTO Users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
                    db.commit()

                    # Log in the user after signup
                    user = User(id=None, name=name, email=email)
                    login_user(user)
                    print('User doesnt exist and has been added to sql table')

                    # Redirect to another page if signup is successful
                    return redirect(url_for('dashboard'))
            except Exception as e:
                print('gone in the except', e)
                # Handle database errors or any other exceptions
                return render_template('signup.html', error="An error occurred during signup. Please try again later.")
            finally:
                cursor.close()
        else:
            print('Passwords dont match')
            return render_template('signup.html', error="Passwords do not match. Please try again.")
    else:
        return render_template('signup.html')


# Check if login exists
def login_exists(email):
    cursor = db.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM Users WHERE email = %s", (email,))
        count = cursor.fetchone()[0]
        return count > 0
    finally:
        cursor.close()

def check_password(email, password):
    cursor = db.cursor()
    try:
        cursor.execute("SELECT password FROM Users WHERE email = %s", (email,))
        hashed_password = cursor.fetchone()
        
        if hashed_password:
            hashed_password_str = hashed_password[0]  # Convert bytes to string
            return check_password_hash(hashed_password_str, password)
    finally:
        cursor.close()
    
    return False


# New routes for authentication
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the email exists in the database
        if login_exists(email):
            # Check if the password matches
            if check_password(email, password):
                # Retreive user information

                cursor = db.cursor()
                cursor.execute("SELECT name FROM Users WHERE email = %s", (email,))
                name = cursor.fetchone()[0]

                cursor.close()
                
                user = User(id=None, name=name, email=email)

                login_user(user)
                print("User logged in: ", user.email)

                next_url = session.get('next', None)
                if next_url:
                    session.pop('next')
                    return redirect(next_url)
                else:
                    return render_template('dashboard.html')
            else:
                error_message = "Incorrect password. Please check your credentials or sign up."
                return render_template('./login.html', error=error_message)
        else:
            error = 'Invalid email or password. Please try again.'
            return render_template('./login.html', error=error)

    elif request.method == 'GET':
        return render_template('login.html')
        
@app.route('/dashboard', methods=['POST', 'GET'])
@login_required
def dashboard():
    return f"Hello! This is your dashboard."


# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)


# # Dynamic recipe options
# selectedCuisine = 'there will be a drop down menu'
# excludedCuisine = 'there will be a drop down menu'
# diet = 'users with accounts can select a specific diet, several options are allowed'
# intolerances = 'users with accounts can select intolerances'
# includeIngredients = 'ingredients that must be used'
# excludeIngredient = 'ingredients that the recipe must not contain'
# recipeNutrition = 'nutrition information included'
# maxReadyTime = 'how long you would like to spend cooking'


#     # 'cuisine': selectedCuisine,
#     # 'excludeCuisine': excludedCuisine,
#     # 'diet': diet,
#     # 'intolerances': intolerances,
#     # 'addRecipeNutrition': recipeNutrition,
#     # 'maxReadyTime': maxReadyTime,
#     'number': 5 