#   ====================================
#   Imports

#   Module that connects python with PostgreSQL database.
import psycopg2
#   Module that enables encryption for passwords.
from cryptography.fernet import Fernet
#   Module used for gitignore.
from conf import cryptography_key, db_username, db_password



#   ====================================
#   globals
f = Fernet(cryptography_key)



def db_connect():
    '''
    Tries connecting to the database. Returns True if successful.
    '''
    global cursor
    global conn
    try:
        conn = psycopg2.connect(dbname='db_levo', user=db_username, host='pgserver.mah.se', password=db_password)
        cursor = conn.cursor()
        return True
    except:
        return False


def db_update_changes():
    '''
    Updates changes made to the database and closes the connection with the database.
    '''
    conn.commit()
    cursor.close()
    conn.close()


def user_exists(username):
    '''
    Returns True if the user exists in the table "users".
    '''
    cursor.execute("SELECT username FROM users WHERE username=%s", (username,))
    if cursor.rowcount != 0:
        return True
    else:
        return False


def email_exists(email):
    '''
    Returns True if the email exists in the table "users".
    '''
    if db_connect():
        cursor.execute("SELECT email FROM users WHERE email=%s", (email,))
        if cursor.rowcount != 0:
            return True
        else:
            return False
    else:
        return "not connected"


def register(user):
    '''
    Encrypts new user's inputed password and inserts the new user's email, username and encrypted password into the "users" table.
    '''
    if db_connect():
        # Tests if the user already exists.
        username = user["username"].lower()
        if user_exists(username):
            return "user exists"
        elif email_exists(username):
            return "username exists as email"

        # Tests if the user's email already exists.
        user_email = user["email"].lower()
        if email_exists(user_email):
            return "email exists"
        if user_exists(user_email):
            return "email exists as username"

        # Self explanatory validations for username and password.
        if len(user["username"]) < 4:
            return "username too short"
        elif len(user["username"]) > 25:
            return "username too long"
        elif len(user["pass"]) < 7:
            return "password too short"
        elif len(user["pass"]) > 25:
            return "password too long"

        # Encrypts the password.
        cyphered_pass = f.encrypt(bytes(user["pass"],encoding='utf8'))

        initial_profile_img = open('./static/img/profile_icon.jpg','rb').read()

        # Inserts the username and cyphered password into the database and commits the changes.
        cursor.execute("INSERT INTO users (email, username, pass, profile_img) VALUES (%s,%s,%s,%s)", (user_email, user["username"], cyphered_pass, psycopg2.Binary(initial_profile_img)))
        db_update_changes()
        return "done"
    else:
        return "not connected"


def login(user):
    '''
    Finds the user in the "users" table. Decrypts the password stored in the table. Compares it to the password inputed by the user and returns the result.
    '''
    if db_connect():
        # Tests if the user exists.
        if not user_exists(user["username"]) and not email_exists(user["username"]):
            return "user does not exist"
        
        # Fetches the user's username and password.
        cursor.execute("SELECT * FROM users WHERE username=%s", (user["username"],))

        if cursor.rowcount == 0:
            cursor.execute("SELECT * FROM users WHERE email=%s", (user["username"],))

        for row in cursor:
            # Decrypts password stored in database.
            pass_from_db = f.decrypt(bytes(row[2]))
            # Validates password
            if bytes(user["pass"],encoding='utf8') == pass_from_db:
                return "password correct"
            else:
                return "password incorrect"
    else:
        return "not connected"


def update_password(user_email, new_password):
    '''
    Stores password in database without validating.
    '''
    if db_connect():
        # Encrypts the password.
        cyphered_pass = f.encrypt(bytes(new_password,encoding='utf8'))
        
        cursor.execute("UPDATE users SET pass=%s WHERE email=%s", (cyphered_pass, user_email))
        db_update_changes()
        return "done"
    else:
        return "not connected"


def change_email(user):
    '''
    Updates database with new email and commits changes.
    '''
    if db_connect():    
        cursor.execute("UPDATE users SET email=%s WHERE username=%s", (user["email"], user["username"]))
        db_update_changes()
        return "done"
    else:
        return "not connected"


def change_pass(user):
    '''
    If password validates it's stored in the database.
    '''
    if db_connect():

        if len(user["new_pass"]) < 7:
            return "password too short"
        elif len(user["new_pass"]) > 25:
            return "password too long"
    
        # Encrypts the password.
        cyphered_pass = f.encrypt(bytes(user["new_pass"],encoding='utf8'))

        # Updates the cyphered password into the database and commits the changes.
        cursor.execute("UPDATE users SET pass=%s WHERE username=%s", (cyphered_pass, user["username"]))
        db_update_changes()
        return "done"
    else:
        return "not connected"


def save_recipe(username, recipe):
    '''
    Stores a recipe for the user in the database.
    '''
    if db_connect():
        # Tests if recipe is already saved.
        cursor.execute("SELECT * FROM saved_recipes WHERE username=%s AND recipe_id=%s", (username, recipe["recipe_id"]))
        if cursor.rowcount != 0:
            return "recipe already saved"

        # Tests if recipe is already stored in database. If not, every attribute of the recipe is stored in the table recipes.
        cursor.execute("SELECT recipe_id FROM recipes WHERE recipe_id=%s", (recipe["recipe_id"],))
        if cursor.rowcount == 0:
            cursor.execute("INSERT INTO recipes (recipe_id, title, image_url, source_url, category) VALUES (%s,%s,%s,%s,%s)", (recipe["recipe_id"], recipe["title"], recipe["image_url"], recipe["source_url"], recipe["category"]))

        # Inserts username and the recipe ID into saved_recipes and commits the changes to the database.
        cursor.execute("INSERT INTO saved_recipes (username, recipe_id) VALUES (%s,%s)", (username, recipe["recipe_id"]))
        db_update_changes()
        return "done"
    else:
        return "not connected"


def remove_recipe(username, recipe):
    '''
    Deletes the row in saved_recipes where the parameters correspond. Commits changes to database.
    '''
    if db_connect():
        cursor.execute("DELETE FROM saved_recipes WHERE username=%s AND recipe_id=%s", (username, recipe["recipe_id"]))
        
        db_update_changes()
        return "done"
    else:
        return "not connected"


def get_saved_recipes(username):
    '''
    Retrieves all recipes saved by the user.
    '''
    if db_connect():

        # Retrieves all columns and rows from the recipes table joined with saved_recipes to get only the recipes stored by the current user.
        cursor.execute("""
        SELECT recipes.recipe_id, title, image_url, source_url, category
            FROM recipes
                JOIN saved_recipes ON saved_recipes.recipe_id = recipes.recipe_id
            WHERE saved_recipes.username = %s
        """, (username,))
        
        if cursor.rowcount == 0:
            return []

        # Turns the result into a list stored with dictionaries where the keys match the data from the database. Then returns the list.
        saved_recipes = []
        for row in cursor:
            recipe = {}
            recipe["recipe_id"] = row[0]
            recipe["title"] = row[1]
            recipe["image_url"] = row[2]
            recipe["source_url"] = row[3]
            recipe["category"] = row[4]
            saved_recipes.append(recipe)
        return saved_recipes
    else:
        return "not connected"


def count_category(username):
    '''
    Counts the amount of recipes stored by the current user, grouped by categories (protein).
    '''
    if db_connect():
        # Declares the initial values of every category to be 0.
        count = {}
        count['meat'] = 0
        count['chicken'] = 0
        count['bird'] = 0
        count['fish'] = 0
        count['seafood'] = 0
        count['veg'] = 0
        
        cursor.execute("""
        SELECT recipes.category, COUNT(saved_recipes.recipe_id)
            FROM recipes
                JOIN saved_recipes ON saved_recipes.recipe_id = recipes.recipe_id
            WHERE saved_recipes.username=%s
        GROUP BY recipes.category
        """, (username,))
        
        if cursor.rowcount == 0:
            return count

        # Feeds the dictonary with the matching data from the database and returns it.
        for row in cursor:
            if row[0] == "meat":
                count['meat'] = row[1]
            if row[0] == "chicken":
                count['chicken'] = row[1]
            if row[0] == "bird":
                count['bird'] = row[1]
            if row[0] == "fish":
                count['fish'] = row[1]
            if row[0] == "seafood":
                count['seafood'] = row[1]
            if row[0] == "veg":
                count['veg'] = row[1]
        
        return count
    else:
        return "not connected"


def check_saved_recipes(username, recipes):
    '''
    Tests if the recipes are already stored by the current user. If a recipe is already stored it gets the attribute "checked",
    if not it gets an empty string. The attribute "checked" represents stared, the empty string represents not stared. Returns
    the recipes in the order they came.
    '''
    if db_connect():
        recipe_saved = []

        for recipe in recipes:
            cursor.execute("SELECT * FROM saved_recipes WHERE username=%s AND recipe_id=%s", (username, recipe["recipe_id"]))
            if cursor.rowcount != 0:
                recipe_saved.append("checked")
            else:
                recipe_saved.append("")

        return recipe_saved
    else:
        return "not connected"


def get_email(username):
    '''
    Returns email from "users" table based on username.
    '''
    if db_connect():
        cursor.execute("SELECT email FROM users WHERE username=%s", (username,))
        for row in cursor:
            return row[0]
    else:
        return "not connected"


def save_profile_img(username, filepath):
    '''
    Stores new_profile_img in database.
    '''
    if db_connect():
        new_profile_img = open('./static/img/new_profile_img.jpg','rb').read()
        cursor.execute("UPDATE users SET profile_img=%s WHERE username=%s", (psycopg2.Binary(new_profile_img), username))
        db_update_changes()
        return "done"
    else:
        return "not connected"


def get_profile_img(username):
    '''
    Selects profile_img from database and writes it in /static/img/profile_img.jpg.
    '''
    if db_connect():
        cursor.execute("SELECT profile_img FROM users WHERE username=%s", (username,))
        row = cursor.fetchone()
        profile_img = row[0]
        open('./static/img/profile_img.jpg', 'wb').write(profile_img)
        return "done"
    else:
        return "not connected"