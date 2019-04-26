#imports
import psycopg2
from cryptography.fernet import Fernet


key = b'CLmBCvpMueiHp0Q9MYhIMObmG6MwhLJ8SisL8iSTTCg='

f = Fernet(key)

def db_connect():
    global cursor
    global conn
    try:
        conn = psycopg2.connect(dbname='db_test_users_ot', user='ai5749', host='pgserver.mah.se', password='amzk822h')
        cursor = conn.cursor()
        return True
    except:
        return False

def db_update_changes():
    conn.commit()
    cursor.close()
    conn.close()

def user_exists(username):
    cursor.execute("SELECT username FROM users WHERE username=%s", (username,))
    if cursor.rowcount != 0:
        return True
    else:
        return False

def insert_new(user):
    if db_connect():
        if user_exists(user["username"]):
            return "user exists"

        cyphered_pass = f.encrypt(bytes(user["pass"],encoding='utf8'))
        cursor.execute("INSERT INTO users (username, pass) VALUES (%s,%s)", (user["username"],cyphered_pass))
        db_update_changes()
        return "done"
    else:
        return "not connected"

def login(user):
    if db_connect():
        if not user_exists(user["username"]):
            return "user does not exist"

        cursor.execute("SELECT * FROM users WHERE username=%s", (user["username"],))

        for row in cursor:
            pass_from_db = f.decrypt(bytes(row[1]))
            if bytes(user["pass"],encoding='utf8') == pass_from_db:
                return "password correct"
            else:
                return "password incorrect"
    else:
        return "not connected"

def save_recipe(username, recipe):
    if db_connect():
        cursor.execute("SELECT * FROM saved_recipes WHERE username=%s AND recipe_id=%s", (username, recipe["recipe_id"]))
        
        if cursor.rowcount != 0:
            return "recipe already saved"

        cursor.execute("INSERT INTO saved_recipes (username, recipe_id) VALUES (%s,%s)", (username, recipe["recipe_id"]))

        cursor.execute("SELECT recipe_id FROM recipes WHERE recipe_id=%s", (recipe["recipe_id"],))
        
        if cursor.rowcount == 0:
            cursor.execute("INSERT INTO recipes (recipe_id, title, image_url, source_url) VALUES (%s,%s,%s,%s)", (recipe["recipe_id"], recipe["title"], recipe["image_url"], recipe["source_url"]))

        db_update_changes()
        return "done"
    else:
        return "not connected"

def get_saved_recipes(username):
    if db_connect():
        cursor.execute("""
        SELECT recipe_id, title, image_url, source_url
            FROM recipes
                JOIN saved_recipes  ON saved_recipes.recipe_id  = recipes.recipe_id
            WHERE saved_recipes.username = %s
        """, (username,))
        
        if cursor.rowcount == 0:
            return "no saved recipes"

        saved_recipes = []
        for row in cursor:
            recipe = {}
            recipe["recipe_id"] = row[0]
            recipe["title"] = row[1]
            recipe["image_url"] = row[2]
            recipe["source_url"] = row[3]
            saved_recipes.append(recipe)
        return saved_recipes
    else:
        return "not connected"