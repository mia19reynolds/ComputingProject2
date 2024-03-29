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

# app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SESSION_PERMANENT'] = True
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Example: session lasts for 7 days
# app.config['SESSION_COOKIE_SECURE'] = True  # Ensure session cookies are only sent over HTTPS
# app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to session cookies

#API key
api_key = "b1950d16d34842d6be06bca4c29ea1fb"

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

login_manager = LoginManager()
login_manager.init_app(app)

# Session(app)

# Define a simple User class for Flask-Login
class User(UserMixin):
    def __init__(self, email, name):
        self.id = email
        self.name = name

@login_manager.user_loader
def load_user(email):
    # Load user from database by name (treated as if it were the id)
    try:

        user_data = readDatabase('*','Users', 'email', email)
        if user_data:
            name = user_data[0]
            user = User(email, name)
            print("User loaded:", user)  # Add this line for debuggings
            return user
    except Exception as e:
        print("NOOOO", e)
        return None
   
    else:
        print("User not found") 
        return None

@app.route('/', methods=['POST', 'GET'])
def index():
    # if not session.get("email"):
    #     return redirect("/")
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    cuisines = [
        'African',
        'Asian',
        'American',
        'British',
        'Cajun',
        'Caribbean',
        'Chinese',
        'Eastern European',
        'European',
        'French',
        'German',
        'Greek',
        'Indian',
        'Irish',
        'Italian',
        'Japanese',
        'Jewish',
        'Korean',
        'Latin American',
        'Mediterranean',
        'Mexican',
        'Middle Eastern',
        'Nordic',
        'Southern',
        'Spanish',
        'Thai',
        'Vietnamese'
    ]
    
    if request.method == 'POST':
        activeUser = current_user.id
        intolerances = readDatabase("intolerances", "User_data", "Email", activeUser)
        query = request.form['query']
        ugh = request.form.getlist('checkbox')
        cuisine = ','.join(ugh)
        print('cuisine:',cuisine)
        return redirect(url_for('search', query=query, cuisine=cuisine))
 
    else:
        # Handle GET requests (e.g., render form)

        try:

            activeUser = current_user.id
            intolerances = readDatabase("intolerances", "User_data", "Email", activeUser)
            query = request.args.get('query')
            cuisine = request.args.get('cuisine')

            # Endpoint URL
            endpoint = 'https://api.spoonacular.com/recipes/complexSearch'

            # Search parameters
            params = {
                'apiKey': api_key,
                'query': query,  # User written input (natural language)
                'cuisine': cuisine,
                'intolerances': intolerances
            }

            print(params)
            # GET request
            response = requests.get(endpoint, params=params)

            # Check if request was successful
            response.raise_for_status()

            # Parse JSON response
            data = response.json()

            results = []

            # Print data recipe titles
            for result in data['results']:
                results.append(result)

            # Return webpage
            return render_template('search.html', cuisine=cuisine, results=results, query=query, cuisines=cuisines)
        
        except Exception as e:
            print('An unexpected error occurred:', e)
            return render_template('search.html')

@app.route('/recipe', methods=['GET', 'POST'])
@login_required
def recipe():
    if request.method == 'GET':
        # Get recipe id from URL parameter
        recipeId = request.args.get('id')

        # Endpoint URL
        endpoint = "https://api.spoonacular.com/recipes/{0}/information".format(recipeId)

        #  Search parameters
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

    elif request.method == 'POST':
        # Handle POST request logic here if needed
        pass  # Placeholder, you can add your POST logic here

    # Optionally, handle unauthorized access here
    return redirect(url_for('login'))  # Redirect unauthenticated users to the login page

    # # Get recipe id from URL parameter
    # recipeId = request.args.get('id')

    # # Endpoint URL
    # endpoint = "https://api.spoonacular.com/recipes/{0}/information".format(recipeId)

    # #  Search paramerters
    # params = {
    #     'apiKey': api_key,
    # }

    # # GET request
    # response = requests.get(endpoint, params=params)

    # # Check if request was successful 
    # if response.status_code == 200:
    #     # Parse JSON response
    #     recipe = response.json()

    #     # Return webpage
    #     return render_template('recipe.html', recipe=recipe)

    # else:
    #     print('Error: ', response.status_code)

# User sign up 
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    # activeUser = current_user.id
    # print("Active User: ", activeUser)
    print('route accessed')
    if request.method == 'POST':
        print('form submitted')
        name = request.form['username']
        email = request.form['email'].lower()
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        print(f"Form data: name={name}, email={email}, password={password}, confirm_password={confirm_password}")

        if password == confirm_password:
            print('Passwords match')
            try:
                # Check if user already exists (email)
                existing_user = readDatabase('*', 'Users', 'LOWER(Email)', email)
                if existing_user:
                    print('User Exists')
                    return render_template('signup.html', error="User with this email already exists. Would you like to <a href='/login'>login</a>?")

                else:
                    hashed_password = generate_password_hash(password).decode('utf-8')
                    cursor = db.cursor()
                    cursor.execute("INSERT INTO Users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
                    db.commit()
                    cursor.close()
                    # Log in the user after signup
                    user = User(email=email, name=name)
                    login_user(user)
                    print('User doesnt exist and has been added to sql table')

                    # Redirect to another page if signup is successful
                    return redirect(url_for('dashboard'))
            except Exception as e:
                print('gone in the except', e)
                # Handle database errors or any other exceptions
                return render_template('signup.html', error="An error occurred during signup. Please try again later.")
        else:
            print('Passwords dont match')
            return render_template('signup.html', error="Passwords do not match. Please try again.")
    else:
        return render_template('signup.html')


# Check if login exists
def login_exists(email):
    cursor = db.cursor()
    try:
        count = readDatabase('COUNT(*)', 'Users', 'email', email)
        if count:
            return True
        else: return False
    finally:
        cursor.close()

def check_password(email, password):
    # cursor = db.cursor()
    try:
        hashed_password = readDatabase('password', 'Users', 'email', email)
        
        if hashed_password:
            hashed_password_str = hashed_password[0]  # Convert bytes to string
            return check_password_hash(hashed_password_str, password)
    except Exception as e:
        print(e)
        return e
    
    return False


# New routes for authentication
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        session["email"] = email

        # Check if the email exists in the database
        if login_exists(email):
            # Check if the password matches
            if check_password(email, password):
                # Retreive user information
                name = readDatabase('name', 'Users', 'email', email)
                
                user = User(email=email, name=name)
                login_user(user)

                print("User logged in: ", user.id)

                return redirect(url_for('dashboard'))

            else:
                error_message = "Incorrect password. Please check your credentials or sign up."
                return render_template('login.html', error=error_message)
        else:
            error = 'Invalid email or password. Please try again.'
            return render_template('login.html', error=error)

    elif request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html')
        
@app.route('/dashboard', methods=['POST', 'GET'])
@login_required
def dashboard():
    activeUser = current_user.id
    print("Active User: ", activeUser)
    print(current_user.is_authenticated)
    print(current_user.is_active)

    print("Current user:", current_user)
    if request.method == 'POST':
        print("Current user:", current_user)
        return render_template('dashboard.html')
    elif request.method == 'GET':
        print("Current user:", current_user)
        return render_template('dashboard.html')

@app.route('/faqs', methods=['GET', 'POST'])
def faqs():

    if request.method == 'POST':
        return render_template('faqs.html')
    elif request.method == 'GET':
        return render_template('faqs.html')

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    activeUser = current_user.id
    print("Active User: ", activeUser)
    if request.method == 'POST':
        return render_template('account.html')
    elif request.method == 'GET':
        return render_template('account.html')


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    activeUser = current_user.id
    print("Active User: ", activeUser)
    if request.method == 'POST':
        print('Settings form submitted')
        intolerances = request.form.getlist('checkbox')
        intolerancesString = ','.join(intolerances)
        print(intolerancesString)
        cursor = db.cursor()
        cursor.execute("UPDATE User_data SET intolerances = %s WHERE Email = %s", (intolerancesString, activeUser))
        db.commit()
        cursor.close()
        return "Settings Applied"
    elif request.method == 'GET':
        return render_template('settings.html')
    
def readDatabase(reqCol, table, column, value):
    print('read:', reqCol, table, column, value)
    try:
        query = 'SELECT {} FROM {} WHERE {} = %s'.format(reqCol, table, column)
        cursor = db.cursor()
        cursor.execute(query, (value,))
        result = cursor.fetchone()
        cursor.close()
        return result
    except Exception as e:
        print('read database error:', e)

def writeDatabase(table, columns, values):
    try:
        query = 'INSERT INTO {} ({}) VALUES ({})'.format(table, columns, values)
        print('write:', query)
        cursor = db.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        return result
    except Exception as e:
        print('write database error:', e)

@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        return redirect(url_for('index'))
    else:
        return render_template('logout.html')

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