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



def get_rnd_ingredient(protein):
    if protein == "dont_know":
        protein = choice(["meat", "bird", "sea", "veg"])
    
    if protein == "meat":
        return choice(meat)
    elif protein == "bird":
        return choice(bird)
    elif protein == "sea":
        return choice(sea)
    else:
        return choice(veg)

def generate_link(protein):
    ingredient = get_rnd_ingredient(protein)
    parameters = {"key": "f47c7ea8d2666c3df9c93d563bd02d72", "q": ingredient}
    response = requests.get("https://www.food2fork.com/api/search", parameters)
    api_content = json.loads(response.content)
    if api_content['count'] == 0:
        print(api_content)
        print(parameters) # if the request generates 0 recipes, we can see why
    api_index = randint(0, (api_content['count']-1))
    return {'source_url': api_content["recipes"][api_index]['source_url'], 'image_url': api_content["recipes"][api_index]['image_url'], 'recipe_id': api_content["recipes"][api_index]['recipe_id']}