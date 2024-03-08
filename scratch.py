import mysql.connector as mysql
import requests
from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)
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

# Define a simple User class for Flask-Login
class User(UserMixin):
    def __init__(self, name, email):
        self.name = name
        self.email = email

@login_manager.user_loader
def load_user(user_name):
    # Load user from database by name (treated as if it were the id)
    cursor = db.cursor()
    cursor.execute("SELECT name, email FROM Users WHERE name = %s", (user_name,))
    user_data = cursor.fetchone()
    if user_data:
        return User(name=user_data[0], email=user_data[1])
    return None

@app.route('/')
def index():
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


# Check if login exists
def login_exists(email, password):
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s OR email = %s", (email, password))
    count = cursor.fetchone()[0]
    cursor.close()
    return count > 0

# New routes for authentication
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # Check if the login exists
    if login_exists(email, password):
        print("Login Exists, reroute to correct page")
        return redirect(url_for('dashboard'))
    else:
        print("Login does not exist in database, either credentials are wrong or user needs to sign up, need to create a  sign up page")
        

@app.route('/dashboard')
@login_required
def dashboard():
    return f"Hello, {current_user.name} ({current_user.email})! This is your dashboard."

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)


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