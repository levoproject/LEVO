#   ====================================
#   Imports
from bottle import route, run, template, request, get, static_file, redirect, TEMPLATE_PATH
from random import choice

try:
    from ReqAPI import generate_link
    api_module_exists = True
except:
    api_module_exists = False

try:
    from DBM import login, register, get_saved_recipes
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
    return template("index", placeholder_current_user=current_user, placeholder_link_0="", placeholder_title_0="", placeholder_img_0="", placeholder_link_1="", placeholder_title_1="", placeholder_img_1="", placeholder_link_2="", placeholder_title_2="", placeholder_img_2="", placeholder_used_ids="", p_m_checked="", p_b_checked="", p_s_checked="", p_v_checked="", p_d_checked="")


@route('/my_profile/')
def my_profile():
    '''
    Returns my_profile.html with empty placeholders.
    '''
    return template("my_profile")


@route('/my_recipes/')
def my_recipes():
    '''
    Returns my_recipes.html with empty placeholders.
    '''
    saved_recipes = get_saved_recipes(current_user)
    return_html = ""
    for recipe in saved_recipes:
        return_html += '<li><a href="' + recipe["source_url"] + '"><label for="' + recipe["recipe_id"] + '">' + recipe["title"] + '</label><br>' + '<img src="' + recipe["image_url"] + '" class="saved_recipes" alt="Image is not available."></a></li>'
    return template("my_recipes", placeholder_saved_recipes=return_html)


@route('/login/')
def login_page():
    '''
    Returns login.html with empty placeholders.
    '''
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
        return "Module DBM is missing or corrupt."

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
        return "Module DBM is missing or corrupt."

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
    Returns about.html with empty placeholders.
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
    proteins = ['meat', 'bird', 'sea', 'veg', 'dont_know']
    chosen_protein = []
    for protein in proteins:
        if request.forms.get(protein) != None:
            chosen_protein.append(request.forms.get(protein))

    #Turns the string used_ids into a list.
    used_ids_list = []
    if used_ids != "":
        used_ids_list = used_ids[1:].split(",")

    #Gets 3 recipes' links, titles, image urls and ID:s.
    if api_module_exists:
        return_recipe = generate_link(chosen_protein, used_ids_list)
    else:
        return "Module ReqAPI is missing or corrupt."
    
    if return_recipe == "error: connection":
        return connection_error_api()

    if return_recipe == "error: limit reached":
        return limit_reached()

    #Controls if recipe nr 1 has already been returned to the user. If not, it's added to the used_ids, else, it loops back.
    for recipe in return_recipe:
        used_ids += "," + recipe['recipe_id']
    
    
    return return_template(chosen_protein, return_recipe, used_ids)


def return_template(chosen_protein, return_recipe, used_ids):
    '''
    Checks the boxes the user checked so that the page looks the same. Then returns index.html with generated links.
    '''
    p_m_checked = ""
    p_b_checked = ""
    p_s_checked = ""
    p_v_checked = ""
    p_d_checked = ""
    if "meat" in chosen_protein:
        p_m_checked = "checked"
    if "bird" in chosen_protein:
        p_b_checked = "checked"
    if "sea" in chosen_protein:
        p_s_checked = "checked"
    if "veg" in chosen_protein:
        p_v_checked = "checked"
    if "dont_know" in chosen_protein:
        p_d_checked = "checked"
    return template("index", placeholder_current_user=current_user, placeholder_used_ids=used_ids, placeholder_link_0=return_recipe[0]["source_url"], placeholder_title_0=return_recipe[0]["title"], placeholder_img_0=return_recipe[0]["image_url"], placeholder_link_1=return_recipe[1]["source_url"], placeholder_title_1=return_recipe[1]["title"], placeholder_img_1=return_recipe[1]["image_url"], placeholder_link_2=return_recipe[2]["source_url"], placeholder_title_2=return_recipe[2]["title"], placeholder_img_2=return_recipe[2]["image_url"], p_m_checked=p_m_checked, p_b_checked=p_b_checked, p_s_checked=p_s_checked, p_v_checked=p_v_checked, p_d_checked=p_d_checked)


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