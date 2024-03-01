import requests
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find_recipe', methods=['POST'])
def process_form():
    user_input = request.form['user_input']
    print('User Input: ', user_input)

    #API key
    api_key = "653ac8f884cb4c99bdd950abd9d769c9"

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

        print(user_input)

        results = []

        # Print data recipe titles
        for result in data['results']:
            print(result['image'])
            results.append(result)
        
        return render_template('find_recipe.html', results=results)

        # return 'Form submitted successfully'

    else:
        print('Error: ', response.status_code)

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