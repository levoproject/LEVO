#   ====================================
#   Imports

#   Module that connects python with HTML.
from bottle import route, run, template, request, get, static_file, redirect, TEMPLATE_PATH, error
#   Imports the choice function used for getting random recipes and generating new passwords.
from random import choice
#   ssl and smtplib are used for sending emails to users. MIMEText and MIMEMultipart are used for email format.
import ssl, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#Imports password for levoproject4@gmail.com from gitignore file.
from conf import levo_password


try:
    #   Module that manages recipes from API.
    from API_requests import generate_link
    api_module_exists = True
except:
    api_module_exists = False

try:
    #   Module that manages the database.
    from DB_module import login, register, get_saved_recipes, save_recipe, check_saved_recipes, remove_recipe, count_category, email_exists, update_password
    db_module_exists = True
except:
    db_module_exists = False


#   ====================================
#   globals
# The user currently logged in. Initially the current_user is set to an empty string which changes when the user logs in.
current_user = ""

# All alternatives for the three questions asked to the user.
proteins = ['meat', 'chicken', 'bird', 'fish', 'seafood', 'veg', 'p_dont_know']
carbs = ['pasta', 'rice', 'potato', 'bread', 'vegetables', 'c_dont_know']

# SSL port, smtp server and LEVO project mail for new_password_email function.
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
levo_email = "projectlevo4@gmail.com"

# Declares relative path to templates.
TEMPLATE_PATH.insert(0, 'views')


@route('/')
@route('/index/')
def index_page():
    '''
    Returns index.html with most placeholders empty.
    '''

    checked_protein = {}
    for protein in proteins:
        checked_protein[protein] = ""

    checked_carb = {}
    for carb in carbs:
        checked_carb[carb] = ""

    return template("index", placeholder_current_user=current_user, placeholder_rid_0="", placeholder_link_0="", placeholder_title_0="", placeholder_img_0="", placeholder_rid_1="", placeholder_link_1="", placeholder_title_1="", placeholder_img_1="", placeholder_link_2="", placeholder_title_2="", placeholder_img_2="", placeholder_rid_2="", placeholder_used_ids="", request=request, recipe_saved_0="", recipe_saved_1="", recipe_saved_2="", placeholder_category="", checked_protein=checked_protein, checked_carb=checked_carb)


@route('/home/')
def home_page():
    return template("home")


@route('/my_profile/')
def my_profile():
    '''
    Returns my_profile.html with the current user.
    '''
    return template("my_profile", placeholder_current_user=current_user)


@route('/my_recipes/')
def my_recipes():
    '''
    Returns my_recipes.html with the user's saved recipes.
    '''
    saved_recipes = get_saved_recipes(current_user)
    
    # Counts the number of recipes stored by the user and groups them by category (protein).
    category_count = count_category(current_user)

    return template("my_recipes", placeholder_current_user=current_user, saved_recipes=saved_recipes, count=category_count, request=request)


@route('/login/')
def login_page():
    '''
    Returns login.html with placeholders set to default.
    '''
    global current_user
    current_user = ""
    return template("login", login=reset_login_placeholders())


def reset_login_placeholders():
    '''
    Sets all login placeholder to its default. Returns dict.
    form 1 represents the login form, form 2 represents the register form and form 3 represents the forgot password form.
    '''
    login = {}
    login["form"] = "1"
    login["error_msg_login"] = ""
    login["error_msg_reg"] = ""
    login["error_msg_forgot"] = ""
    login["username_login"] = ""
    login["email_reg"] = ""
    login["username_reg"] = ""
    login["email_forgot"] = ""

    return login


@route('/logout/')
def logout():
    '''
    Redirects to the route '/login/'. In the login_page function the current user is set to none.
    '''
    return redirect('/login/')


@route('/login_form/', method='POST')
def login_form():
    '''
    Authenticates the username and password and returns either error messages or redirects to /index/.
    '''
    global current_user
    # Requests the username and password inputs from the login form.
    user = {}
    user["username"] = request.forms.get('log_username')
    user["pass"] = request.forms.get('log_password')

    if db_module_exists:
        # Calls login function in DB_module to authenticate the username and password.
        result = login(user)
    else:
        return "DB_module is missing or corrupt."


    if result == "not connected":
        return connection_error_db()
    
    elif result == "user does not exist":
        return return_error_login("There is no user with this username!", user)

    elif result == "password incorrect":
        return return_error_login("The password is incorrect!", user)

    elif result == "password correct":
        current_user = user["username"]

        return redirect('/')


def return_error_login(msg, user):
    login = reset_login_placeholders()
        
    login['error_msg_login'] = msg
    login['username_login'] = user["username"]

    return template("login", login=login)


@route('/register_form/', method='POST')
def register_form():
    '''
    Validates the username and password and returns either error messages or redirects to /index/.
    '''
    global current_user
    user = {}
    # Requests the username and password inputs from the register form.
    user["username"] = request.forms.get('reg_username')
    user["pass"] = request.forms.get('reg_password')
    user["email"] = request.forms.get('reg_email')

    if db_module_exists:
        # Calls register function in DB_module to validate the username and password.
        result = register(user)
    else:
        return "DB_module is missing or corrupt."


    if result == "not connected":
        return connection_error_db()

    elif result == "user exists" or result == "username exists as email":
        return return_error_reg("This username is already taken!", user)

    elif result == "email exists" or result == "email exists as username":
        return return_error_reg("This email is already taken!", user)

    elif result == "username too short":
        return return_error_reg("Your username must have at least 4 characters!", user)

    elif result == "username too long":
        return return_error_reg("Your username can have a maximum of 25 characters!", user)

    elif result == "password too short":
        return return_error_reg("Your password must have at least 7 characters!", user)

    elif result == "password too long":
        return return_error_reg("Your password can have a maximum of 25 characters!", user)

    elif result == "done":
        current_user = user["username"]
        return redirect('/')


def return_error_reg(msg, user):
    login = reset_login_placeholders()
    
    login['form'] = "2"
    login['error_msg_reg'] = msg
    login['username_reg'] = user["username"]

    return template("login", login=login)


@route('/forgot_pass_form/', method='POST')
def forgot_pass_form():
    '''
    
    '''
    # Requests the email input from the forgot password form.
    user_email = request.forms.get('forgot_email')

    if db_module_exists:
        # Calls register function in DB_module to validate the username and password.
        result = email_exists(user_email)
    else:
        return "DB_module is missing or corrupt."

    if result == "not connected":
        return connection_error_db()
    elif result == True:
        return new_password_email(user_email)
    else:
        return return_error_forgot("Email does not exist", user_email)


def return_error_forgot(msg, user_email):
    login = reset_login_placeholders()
    
    login['form'] = "3"
    login['error_msg_forgot'] = msg
    login['email_forgot'] = user_email

    return template("login", login=login)


def new_password_email(user_email):
    new_password = generate_password()

    result = update_password(user_email, new_password)

    if result == "not connected":
        return connection_error_db()
    
    elif result == "done":
        message = MIMEMultipart("alternative")
        message["Subject"] = "New Password"
        message["From"] = levo_email
        message["To"] = user_email

        html = """\
        <p id="new_pass_p">Your new password is: %s</p>
        """ % (new_password)

        css = """
        <style>
            #new_pass_p {
                padding: 30px;
                border: solid #555 2px;
                background-color: lightcyan;
                color: darkgreen;
                display: inline-block;
                font-size: 24px;
            }
        </style>
        """

        content = html + css
        html_part = MIMEText(content, "html")
        message.attach(html_part)

        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(levo_email, levo_password)
            
            server.sendmail(levo_email, user_email, message.as_string())
        
        return redirect('/login/')


def generate_password():
    password = ""
    for i in range(0,12):
        password += choice(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm'])
    return password


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

    # Gets the ID:s of all already generated results.
    used_ids = request.forms.get('used_ids')

    # Fills the list chosen_protein with the value of every box checked by the user.
    chosen_protein = []
    for protein in proteins:
        if request.forms.get(protein) != None:
            chosen_protein.append(request.forms.get(protein))

    # Fills the list chosen_carb with the value of every box checked by the user.
    chosen_carb = []
    for carb in carbs:
        if request.forms.get(carb) != None:
            chosen_carb.append(request.forms.get(carb))

    # Turns the string used_ids into a list.
    used_ids_list = []
    if used_ids != "":
        used_ids_list = used_ids[1:].split(",")

    # Gets 3 recipes' links, titles, image urls and ID:s.
    if api_module_exists:
        return_recipe = generate_link(chosen_protein, chosen_carb, used_ids_list)
    else:
        return "Module ReqAPI is missing or corrupt."

    # Checks if different errors has been returned
    if return_recipe == "error: connection":
        return connection_error_api()
    elif return_recipe == "error: limit reached":
        return limit_reached()

    # Adds the ID:s of the recipes returned to used_ids.
    for recipe in return_recipe:
        used_ids += "," + recipe['recipe_id']
    
    # If a user is logged in check_saved_recipes is called in DB_module. If the returned recipes are already saved by the user they will be 
    # automatically stared. If the user is not logged in the recipes won't be stared.
    if current_user != "":
        recipes_saved = check_saved_recipes(current_user, return_recipe)
    else:
        recipes_saved = ["","",""]
    
    return return_template(chosen_protein, chosen_carb, return_recipe, used_ids, recipes_saved)


def return_template(chosen_protein, chosen_carb, return_recipe, used_ids, recipes_saved):
    '''
    Checks the boxes the user checked so that the page looks the same when going back. Then returns index.html with generated links.
    '''

    checked_protein = {}
    for protein in proteins:
        checked_protein[protein] = ""

    for protein in chosen_protein:
        checked_protein[protein] = "checked"


    checked_carb = {}
    for carb in carbs:
        checked_carb[carb] = ""

    for carb in chosen_carb:
        checked_carb[carb] = "checked"


    return template("index", placeholder_current_user=current_user, placeholder_used_ids=used_ids, placeholder_category=return_recipe[0]["category"], placeholder_rid_0=return_recipe[0]["recipe_id"], placeholder_link_0=return_recipe[0]["source_url"], placeholder_title_0=return_recipe[0]["title"], placeholder_img_0=return_recipe[0]["image_url"], placeholder_rid_1=return_recipe[1]["recipe_id"], placeholder_link_1=return_recipe[1]["source_url"], placeholder_title_1=return_recipe[1]["title"], placeholder_img_1=return_recipe[1]["image_url"], placeholder_rid_2=return_recipe[2]["recipe_id"], placeholder_link_2=return_recipe[2]["source_url"], placeholder_title_2=return_recipe[2]["title"], placeholder_img_2=return_recipe[2]["image_url"], request=request, recipe_saved_0=recipes_saved[0], recipe_saved_1=recipes_saved[1], recipe_saved_2=recipes_saved[2], checked_protein=checked_protein, checked_carb=checked_carb)


@route('/star_recipe')
def star_recipe():
    '''
    When the user stars a recipe the recipe-data is gathered to be put in database.
    '''
    recipe = {}
    recipe["recipe_id"] = request.params.get('recipe_id', 0, type=str)
    recipe["title"] = request.params.get('title', 0, type=str)
    recipe["source_url"] = request.params.get('source_url', 0, type=str)
    recipe["image_url"] = request.params.get('image_url', 0, type=str)
    recipe["category"] = request.params.get('category', 0, type=str)

    # Calls the save_recipe function in DB_module.
    save_recipe(current_user, recipe)


@route('/remove_star_recipe')
def remove_star_recipe():
    '''
    When the star is removed from a recipe the row containing the current user's username and the recipe's ID is removed from the table
    saved_recipes in the database.
    '''
    recipe = {}
    # The recipe's ID is requested.
    recipe["recipe_id"] = request.params.get('recipe_id', 0, type=str)

    # Calls the remove_recipe function in DB_module.    
    remove_recipe(current_user, recipe)


@error(404)
def error404(error):
    '''
    If the page is not found error.html is returned to the user.
    '''
    return template('error')


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


# Runs the web server with the address http://localhost:8080/.
run(host='localhost', port=8080, debug=True)