#   ====================================
#   Imports
import requests
import json
from random import randint, choice



#   ====================================
#   globals
meat = ['beef', 'pork', 'lamb', 'mutton', 'venison', 'bison', 'boar', 'rabbit']
bird = ['chicken', 'duck', 'turkey', 'goose', 'pheasant', 'pigeon']
sea = ['fish', 'salmon', 'tuna', 'mackerel', 'cod', 'sardines', 'herring', 'perch', 'anchovy', 'lobster', 'crawfish', 'crayfish', 'prawns', 'shrimps', 'crab', 'squid', 'scallops', 'clams', 'oysters', 'mussels']
veg = ['vegetarian', 'vegan']



def get_rnd_ingredient(chosen_protein):
    '''
    Gets random ingredient based on the chosen protein.
    '''

    #If the user has checked the box "I'm not sure!", a random protein is chosen. Else a random protein of every box checked is chosen.
    if "dont_know" in chosen_protein or chosen_protein == []:
        chosen_protein = choice(["meat", "bird", "sea", "veg"])
    else:
        chosen_protein = choice(chosen_protein)

    #Returns a random ingredient based on the chosen_protein.
    if chosen_protein == "meat":
        return choice(meat)
    elif chosen_protein == "bird":
        return choice(bird)
    elif chosen_protein == "sea":
        return choice(sea)
    else:
        return choice(veg)

def generate_link(chosen_protein):
    '''
    Makes an API request based on the users preferences. Of the result, 3 recipes are chosen att random and specific values of these recipes are returned.
    '''
    ingredient = get_rnd_ingredient(chosen_protein)

    #Makes a get request with our API-key and the randomized ingredient as parameters.
    parameters = {"key": "f47c7ea8d2666c3df9c93d563bd02d72", "q": ingredient}
    response = requests.get("https://www.food2fork.com/api/search", parameters)
    api_content = json.loads(response.content)

    #If the API-request limit is reached the result will be: {'error': 'limit'}.
    if api_content == {'error': 'limit'}:
        return "error: limit reached"
    
    #If the request generates 0 recipes, we can see why
    if api_content['count'] == 0:
        print(api_content)
        print(parameters)

    #Chooses a random recipe of the amount returned from the request. Then returns 3 of them.
    api_index = randint(0, (api_content['count']-2))
    return [{'source_url': api_content["recipes"][api_index]['source_url'], 'title': api_content["recipes"][api_index]['title'], 'image_url': api_content["recipes"][api_index]['image_url'], 'recipe_id': api_content["recipes"][api_index]['recipe_id']}, {'source_url': api_content["recipes"][api_index - 1]['source_url'], 'title': api_content["recipes"][api_index - 1]['title'], 'image_url': api_content["recipes"][api_index - 1]['image_url'], 'recipe_id': api_content["recipes"][api_index - 1]['recipe_id']}, {'source_url': api_content["recipes"][api_index + 1]['source_url'], 'title': api_content["recipes"][api_index + 1]['title'], 'image_url': api_content["recipes"][api_index + 1]['image_url'], 'recipe_id': api_content["recipes"][api_index + 1]['recipe_id']}]