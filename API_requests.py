#   ====================================
#   Imports

#   Module that makes requests to the API.
import requests
#   Module that stores data, used when requesting recipes from API.
import json
#   Imports the API key from gitignore file.
from conf import f2f_api_key
#   Imports the random function used for getting random recipes and ingredients.
from random import randint, choice



#   ====================================
#   globals

#   Lists containing ingredients for every available protein.
meat = ['beef', 'pork', 'lamb', 'mutton', 'bison']
chicken = ['chicken']
bird = ['duck', 'turkey', 'goose', 'pheasant', 'pigeon']
fish = ['fish', 'salmon', 'tuna', 'mackerel', 'cod', 'sardines', 'herring', 'perch', 'anchovy']
seafood = ['lobster', 'crawfish', 'crayfish', 'prawns', 'shrimps', 'crab', 'squid', 'scallops', 'clams', 'oysters', 'mussels']
game = ['venison', 'boar', 'rabbit']
veg = ['vegetarian', 'vegan']

#   Lists containing ingredients for every available carb.
pasta = ['pasta', 'noodles', 'noodle', 'spaghetti', 'tortellini', 'fettucine', 'rigatoni', 'penne', 'tagliatelle', 'linguine', 'lasagna', 'lasagne', 'pappardelle', 'macaroni', 'farfalle', 'fusilli', 'gnocchi', '	maccheroni', 'cannelloni', 'ravioli', 'tortelloni', 'tortelli', 'lasagnette', 'bucatini']
rice = ['rice']
potato = ['potato']
bread = ['bread', 'pita', 'sourdough', 'tortilla', 'pizza']
vegetables = ['broccoli', 'cauliflower', 'salad', 'asparagus', 'tomato', 'cucumber', 'carrots', 'tomatoes', 'avocado', 'onion', 'onions', 'leek', 'beans', 'chickpeas', 'peas', 'cabbage', 'kale', 'pepper', 'peppers', 'aubergine', 'lettuce', 'beets', 'parsnips', 'eggplants', 'eggplant', 'mushrooms', 'shitaake', 'portabello', 'button mushrooms', 'brussel', 'sprouts' 'lentals']


def get_rnd_protein(chosen_protein):
    '''
    Gets random ingredient based on the chosen protein.
    '''

    #If the user has checked the box "I'm not sure!", a random protein is chosen. Else a random protein of every box checked is chosen.
    if "p_dont_know" in chosen_protein or chosen_protein == []:
        chosen_protein = choice(["meat", "chicken", "bird", "fish", "seafood", "game", "veg"])
    else:
        chosen_protein = choice(chosen_protein)

    #Returns a random ingredient based on the chosen_protein.
    if chosen_protein == "meat":
        return choice(meat)
    elif chosen_protein == "chicken":
        return choice(chicken)
    elif chosen_protein == "bird":
        return choice(bird)
    elif chosen_protein == "fish":
        return choice(fish)
    elif chosen_protein == "seafood":
        return choice(seafood)
    elif chosen_protein == "game":
        return choice(game)
    else:
        return choice(veg)


def get_rnd_carb(chosen_carb):
    '''
    Gets random ingredient based on the chosen carb.
    '''

    #If the user has checked the box "I don't have any preferences!", a random carb is chosen. Else a random carb of every box checked is chosen.
    if "c_dont_know" in chosen_carb or chosen_carb == []:
        chosen_carb = choice(["pasta", "rice", "potato", "bread", "vegetables"])
    else:
        chosen_carb = choice(chosen_carb)

    #Returns a random ingredient based on the chosen carb.
    if chosen_carb == "pasta":
        return choice(pasta)
    elif chosen_carb == "rice":
        return choice(rice)
    elif chosen_carb == "potato":
        return choice(potato)
    elif chosen_carb == "bread":
        return choice(bread)
    else:
        return choice(vegetables)


def get_response(parameters):
    '''
    Makes the API request and returns either the result or error: connection.
    '''
    try:
        return requests.get("https://www.food2fork.com/api/search", parameters)
    except:
        return "error: connection"


def get_rnd_index(api_content, used_ids):
    '''
    Returns 3 indexes to be used on api_content while making sure there's no duplicates and the recipe of the randomized index has not been used before.
    '''
    api_index = []

    for i in range(0,3):
        while True:
            temp_index = randint(0, (api_content['count'] - 1))
            
            if temp_index not in api_index:
                if api_content["recipes"][temp_index]['recipe_id'] not in used_ids:
                    api_index.append(temp_index)
                    break
    
    return api_index


def generate_link(chosen_protein, chosen_carb, used_ids):
    '''
    Makes an API request based on the users preferences. Of the result, 3 recipes are chosen att random and specific values of these recipes are returned.
    '''
    ingredients = []
    ingredients.append(get_rnd_protein(chosen_protein))
    ingredients.append(get_rnd_carb(chosen_carb))

    ingredients_str = ingredients[0] + "," + ingredients[1]

    #Makes a get request with our API-key and the randomized ingredient as parameters.
    parameters = {"key": f2f_api_key, "q": ingredients_str}
    response = get_response(parameters)

    #If the API-server can't be reached, error: connection is returned.
    if response == "error: connection":
        return "error: connection"

    api_content = json.loads(response.content)

    #If the API-request limit is reached the result will be: {'error': 'limit'}.
    if api_content == {'error': 'limit'}:
        return "error: limit reached"
    
    #If the request generates 0 recipes, we can see why
    if api_content['count'] == 0:
        print(api_content)
        print(parameters)

    #Chooses a random recipe of the amount returned from the request. Then returns 3 of them.
    api_index = get_rnd_index(api_content, used_ids)
    return [{'source_url': api_content["recipes"][api_index[0]]['source_url'], 'title': api_content["recipes"][api_index[0]]['title'], 'image_url': api_content["recipes"][api_index[0]]['image_url'], 'recipe_id': api_content["recipes"][api_index[0]]['recipe_id']}, {'source_url': api_content["recipes"][api_index[1]]['source_url'], 'title': api_content["recipes"][api_index[1]]['title'], 'image_url': api_content["recipes"][api_index[1]]['image_url'], 'recipe_id': api_content["recipes"][api_index[1]]['recipe_id']}, {'source_url': api_content["recipes"][api_index[2]]['source_url'], 'title': api_content["recipes"][api_index[2]]['title'], 'image_url': api_content["recipes"][api_index[2]]['image_url'], 'recipe_id': api_content["recipes"][api_index[2]]['recipe_id']}]