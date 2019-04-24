#   ====================================
#   Imports
import bottle
from bottle import route, run, template, request, get, static_file
from random import choice
import ReqAPI



#   ====================================
#   globals



bottle.TEMPLATE_PATH.insert(0, 'views')


@route('/')
@route('/index/')
def index_page():
    '''
    Returns index.html with empty placeholders.
    '''
    return template("index", placeholder_used_ids="", placeholder_hidden="hidden", p_m_checked="", p_b_checked="", p_s_checked="", p_v_checked="", p_d_checked="")

@route('/result/')
def result_page():
    '''
    Returns result.html with placeholders with empty results placeholders.
    '''
    return template("result",  placeholder_link_0="", placeholder_title_0="", placeholder_img_0="", placeholder_link_1="", placeholder_title_1="", placeholder_img_1="", placeholder_link_2="", placeholder_title_2="", placeholder_img_2="",)

@route('/generate/',method='POST')
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

    while True:
        #Gets 3 recipes' links, titles, image urls and ID:s.
        return_recipe = ReqAPI.generate_link(chosen_protein)
        
        if return_recipe == "error: connection":
            return connection_error()

        if return_recipe == "error: limit reached":
            return limit_reached()
        
        #Controls if recipe nr 1 has already been returned to the user. If not, it's added to the used_ids, else, it loops back.
        if return_recipe[0]['recipe_id'] not in used_ids_list:
            used_ids += "," + return_recipe[0]['recipe_id']
            break
    
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
    return template("index", placeholder_used_ids=used_ids, placeholder_link_0=return_recipe[0]["source_url"], placeholder_title_0=return_recipe[0]["title"], placeholder_img_0=return_recipe[0]["image_url"], placeholder_link_1=return_recipe[1]["source_url"], placeholder_title_1=return_recipe[1]["title"], placeholder_img_1=return_recipe[1]["image_url"], placeholder_link_2=return_recipe[2]["source_url"], placeholder_title_2=return_recipe[2]["title"], placeholder_img_2=return_recipe[2]["image_url"], placeholder_hidden="", p_m_checked=p_m_checked, p_b_checked=p_b_checked, p_s_checked=p_s_checked, p_v_checked=p_v_checked, p_d_checked=p_d_checked)


def limit_reached():
    '''
    The message shown to the user if the API request limit is reached.
    '''
    return 'API request limit reached. This web application is still under development. We are using an API(application programming interface) to generate results. The API we are utilizing is free and intended for developing purposes. Therefore there is a daily limit to the number of results we are able to request.'


def connection_error():
    '''
    The message shown to the user if ReqAPI can't connect to the API.
    '''
    return "Can't connect to API server."


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