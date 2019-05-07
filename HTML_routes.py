#   ====================================
#   Imports

#   Module that connects python with HTML.
from bottle import route, run, template, request, get, static_file, redirect, TEMPLATE_PATH
#   Imports the random function used for getting random recipes.
from random import choice
import json

try:
    #   Module that manages recipes from API.
    from API_requests import generate_link
    api_module_exists = True
except:
    api_module_exists = False

try:
    from DB_module import login, register, get_saved_recipes, save_recipe, check_saved_recipes, remove_recipe
    db_module_exists = True
except:
    db_module_exists = False


#   ====================================
#   globals
current_user = ""



TEMPLATE_PATH.insert(0, 'views')


@route('/')
@route('/index/')
def index_page():
    '''
    Returns index.html with empty placeholders.
    '''
    return template("index", placeholder_current_user=current_user, placeholder_rid_0="", placeholder_link_0="", placeholder_title_0="", placeholder_img_0="", placeholder_rid_1="", placeholder_link_1="", placeholder_title_1="", placeholder_img_1="", placeholder_link_2="", placeholder_title_2="", placeholder_img_2="", placeholder_rid_2="", placeholder_used_ids="", meat_checked="", chicken_checked="", bird_checked="", fish_checked="", seafood_checked="", game_checked="", veg_checked="", p_dont_know_checked="", pasta_checked="", rice_checked="", potato_checked="", bread_checked="", vegetables_checked="", c_dont_know_checked="", request=request, recipe_saved_0="", recipe_saved_1="", recipe_saved_2="", placeholder_category="")


@route('/my_profile/')
def my_profile():
    '''
    Returns my_profile.html with empty placeholders.
    '''
    return template("my_profile", placeholder_current_user=current_user)


@route('/my_recipes/')
def my_recipes():
    '''
    Returns my_recipes.html with empty placeholders.
    '''
    saved_recipes = get_saved_recipes(current_user)

    return template("my_recipes", placeholder_current_user=current_user, saved_recipes=saved_recipes)


@route('/login/')
def login_page():
    '''
    Returns login.html with empty placeholders.
    '''
    return template("login", placeholder_form="1", placeholder_error_msg_login="", placeholder_error_msg_reg="", placeholder_username_login="", placeholder_pass_login="", placeholder_username_reg="", placeholder_pass_reg="")


@route('/logout/')
def logout():
    '''
    Returns login.html with empty placeholders. Sets current_user to none.
    '''
    current_user = ""
    return template("login", placeholder_form="1", placeholder_error_msg_login="", placeholder_error_msg_reg="", placeholder_username_login="", placeholder_pass_login="", placeholder_username_reg="", placeholder_pass_reg="")



@route('/login_form/', method='POST')
def login_form():
    '''

    '''
    global current_user
    user = {}
    user["username"] = request.forms.get('log_username')
    user["pass"] = request.forms.get('log_password')

    if db_module_exists:
        result = login(user)
    else:
        return "DB_module is missing or corrupt."

    if result == "not connected":
        return connection_error_db()
    elif result == "user does not exist":
        return template("login", placeholder_form="1", placeholder_error_msg_login="There is no user with this username!", placeholder_error_msg_reg="", placeholder_username_login=user["username"], placeholder_pass_login="", placeholder_username_reg="", placeholder_pass_reg="")
    elif result == "password incorrect":
        return template("login", placeholder_form="1", placeholder_error_msg_login="The password is incorrect!", placeholder_error_msg_reg="", placeholder_username_login=user["username"], placeholder_pass_login="", placeholder_username_reg="", placeholder_pass_reg="")
    elif result == "password correct":
        current_user = user["username"]
        return redirect('/')


@route('/register_form/', method='POST')
def register_form():
    '''

    '''
    global current_user
    user = {}
    user["username"] = request.forms.get('reg_username')
    user["pass"] = request.forms.get('reg_password')

    if db_module_exists:
        result = register(user)
    else:
        return "DB_module is missing or corrupt."

    if result == "not connected":
        return connection_error_db()
    elif result == "user exists":
        return template("login", placeholder_form="2", placeholder_error_msg_login="", placeholder_error_msg_reg="This username is already taken!", placeholder_username_login="", placeholder_pass_login="", placeholder_username_reg=user["username"], placeholder_pass_reg="")
    elif result == "username too short":
        return template("login", placeholder_form="2", placeholder_error_msg_login="", placeholder_error_msg_reg="Your username must have at least 4 characters!", placeholder_username_login="", placeholder_pass_login="", placeholder_username_reg=user["username"], placeholder_pass_reg="")
    elif result == "username too long":
        return template("login", placeholder_form="2", placeholder_error_msg_login="", placeholder_error_msg_reg="Your username can have a maximum of 25 characters!", placeholder_username_login="", placeholder_pass_login="", placeholder_username_reg=user["username"], placeholder_pass_reg="")
    elif result == "password too short":
        return template("login", placeholder_form="2", placeholder_error_msg_login="", placeholder_error_msg_reg="Your password must have at least 7 characters!", placeholder_username_login="", placeholder_pass_login="", placeholder_username_reg=user["username"], placeholder_pass_reg="")
    elif result == "password too long":
        return template("login", placeholder_form="2", placeholder_error_msg_login="", placeholder_error_msg_reg="Your password can have a maximum of 25 characters!", placeholder_username_login="", placeholder_pass_login="", placeholder_username_reg=user["username"], placeholder_pass_reg="")
    elif result == "done":
        current_user = user["username"]
        return redirect('/')


@route('/about/')
def about_page():
    '''
    Returns about.html.
    '''
    return template("about", placeholder_current_user=current_user)


@route('/generate/', method='POST')
def generate_recipe():
    '''
    Generates a random result based on the chosen protein.
    '''

    #Gets the ID:s of all already generated results.
    used_ids = request.forms.get('used_ids')

    #Fills the list chosen_protein with the value of every box checked by the user.
    proteins = ['meat', 'chicken', 'bird', 'fish', 'seafood', 'game', 'veg', 'p_dont_know']
    chosen_protein = []
    for protein in proteins:
        if request.forms.get(protein) != None:
            chosen_protein.append(request.forms.get(protein))

    #Fills the list chosen_carb with the value of every box checked by the user.
    carbs = ['pasta', 'rice', 'potato', 'bread', 'vegetables', 'c_dont_know']
    chosen_carb = []
    for carb in carbs:
        if request.forms.get(carb) != None:
            chosen_carb.append(request.forms.get(carb))

    #Turns the string used_ids into a list.
    used_ids_list = []
    if used_ids != "":
        used_ids_list = used_ids[1:].split(",")

    #Gets 3 recipes' links, titles, image urls and ID:s.
    if api_module_exists:
        return_recipe = generate_link(chosen_protein, chosen_carb, used_ids_list)
    else:
        return "Module ReqAPI is missing or corrupt."
    
    if return_recipe == "error: connection":
        return connection_error_api()

    if return_recipe == "error: limit reached":
        return limit_reached()

    for recipe in return_recipe:
        used_ids += "," + recipe['recipe_id']
    
    if current_user != "":
        recipes_saved = check_saved_recipes(current_user, return_recipe)
    else:
        recipes_saved = ["","",""]
    
    return return_template(chosen_protein, chosen_carb, return_recipe, used_ids, recipes_saved)


def return_template(chosen_protein, chosen_carb, return_recipe, used_ids, recipes_saved):
    '''
    Checks the boxes the user checked so that the page looks the same. Then returns index.html with generated links.
    '''
    meat_checked = ""
    chicken_checked = ""
    bird_checked = ""
    fish_checked = ""
    seafood_checked = ""
    game_checked = ""
    veg_checked = ""
    p_dont_know_checked = ""

    pasta_checked= ""
    rice_checked= ""
    potato_checked= ""
    bread_checked= ""
    vegetables_checked= ""
    c_dont_know_checked = ""


    if "meat" in chosen_protein:
        meat_checked = "checked"
    
    if "chicken" in chosen_protein:
        chicken_checked = "checked"
    
    if "bird" in chosen_protein:
        bird_checked = "checked"
    
    if "fish" in chosen_protein:
        fish_checked = "checked"
    
    if "seafood" in chosen_protein:
        seafood_checked = "checked"
    
    if "game" in chosen_protein:
        game_checked = "checked"
    
    if "veg" in chosen_protein:
        veg_checked = "checked"
    
    if "p_dont_know" in chosen_protein:
        p_dont_know_checked = "checked"


    if "pasta" in chosen_carb:
        pasta_checked = "checked"

    if "rice" in chosen_carb:
        rice_checked = "checked"

    if "potato" in chosen_carb:
        potato_checked = "checked"

    if "bread" in chosen_carb:
        bread_checked = "checked"

    if "bread" in chosen_carb:
        bread_checked = "checked"

    if "vegetables" in chosen_carb:
        vegetables_checked = "checked"

    if "c_dont_know" in chosen_carb:
        c_dont_know_checked = "checked"


    return template("index", placeholder_current_user=current_user, placeholder_used_ids=used_ids, placeholder_category=return_recipe[0]["category"], placeholder_rid_0=return_recipe[0]["recipe_id"], placeholder_link_0=return_recipe[0]["source_url"], placeholder_title_0=return_recipe[0]["title"], placeholder_img_0=return_recipe[0]["image_url"], placeholder_rid_1=return_recipe[1]["recipe_id"], placeholder_link_1=return_recipe[1]["source_url"], placeholder_title_1=return_recipe[1]["title"], placeholder_img_1=return_recipe[1]["image_url"], placeholder_rid_2=return_recipe[2]["recipe_id"], placeholder_link_2=return_recipe[2]["source_url"], placeholder_title_2=return_recipe[2]["title"], placeholder_img_2=return_recipe[2]["image_url"], meat_checked=meat_checked, chicken_checked=chicken_checked, bird_checked=bird_checked, fish_checked=fish_checked, seafood_checked=seafood_checked, game_checked=game_checked, veg_checked=veg_checked, p_dont_know_checked=p_dont_know_checked, pasta_checked=pasta_checked, rice_checked=rice_checked, potato_checked=potato_checked, bread_checked=bread_checked, vegetables_checked=vegetables_checked, c_dont_know_checked=c_dont_know_checked, request=request, recipe_saved_0=recipes_saved[0], recipe_saved_1=recipes_saved[1], recipe_saved_2=recipes_saved[2])


@route('/star_recipe')
def star_recipe():

    recipe = {}
    recipe["recipe_id"] = request.params.get('recipe_id', 0, type=str)
    recipe["title"] = request.params.get('title', 0, type=str)
    recipe["source_url"] = request.params.get('source_url', 0, type=str)
    recipe["image_url"] = request.params.get('image_url', 0, type=str)
    recipe["category"] = request.params.get('category', 0, type=str)

    save_recipe(current_user, recipe)
    
    return json.dumps({'result': 'Recipe Saved'})


@route('/remove_star_recipe')
def remove_star_recipe():

    recipe = {}
    recipe["recipe_id"] = request.params.get('recipe_id', 0, type=str)

    remove_recipe(current_user, recipe)
    
    return json.dumps({'result': 'Recipe Removed'})


def limit_reached():
    '''
    The message shown to the user if the API request limit is reached.
    '''
    return 'API request limit reached. This web application is still under development. We are using an API(application programming interface) to generate results. The API we are utilizing is free and intended for developing purposes. Therefore there is a daily limit to the number of results we are able to request.'


def connection_error_api():
    '''
    The message shown to the user if ReqAPI can't connect to the API.
    '''
    return "Can't connect to API server."


def connection_error_db():
    '''
    The message shown to the user if DBM can't connect to the database server.
    '''
    return "Can't connect to database server."


@route("/static/css/<filename>")
def static_files_css(filename):
	'''
	Returns static files from the folder "static".
	'''
	return static_file(filename, root="static/css")


@route("/static/img/<filename>")
def static_files_img(filename):
	'''
	Returns static files from the folder "img".
	'''
	return static_file(filename, root="static/img")


@route("/static/js/<filename>")
def static_files_js(filename):
	'''
	Returns static files from the folder "js".
	'''
	return static_file(filename, root="static/js")


#Runs the web server with the address http://localhost:8080/.
run(host='localhost', port=8080, debug=True)