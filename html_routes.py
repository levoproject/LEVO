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
    Retunerar index.html med tomma placeholders.
    '''
    return template("index", placeholder_link_0="", placeholder_title_0="", placeholder_img_0="", placeholder_link_1="", placeholder_title_1="", placeholder_img_1="", placeholder_link_2="", placeholder_title_2="", placeholder_img_2="", placeholder_used_ids="", placeholder_hidden="hidden", p_m_checked="", p_b_checked="", p_s_checked="", p_v_checked="", p_d_checked="")


@route('/generate/',method='POST')
def generate_recipe():
    '''
    Genererar en slumpmässigt länk utifrån valet av protein.
    '''
    proteins = ['meat', 'bird', 'sea', 'veg', 'dont_know']
    chosen_protein = []
    used_ids = request.forms.get('used_ids')
    for protein in proteins:
        if request.forms.get(protein) != None:
            chosen_protein.append(request.forms.get(protein))

    used_ids_list = []
    if used_ids != "":
        used_ids_list = used_ids[1:].split(",")

    while True:
        return_recipe = ReqAPI.generate_link(chosen_protein)
        
        if return_recipe == "error: limit reached":
            return limit_reached()
        
        if return_recipe[0]['recipe_id'] not in used_ids_list:
            used_ids += "," + return_recipe[0]['recipe_id']
            break
    
    return return_template(chosen_protein, return_recipe, used_ids)


def return_template(chosen_protein, return_recipe, used_ids):
    p_m_checked = ""
    p_b_checked = ""
    p_s_checked = ""
    p_v_checked = ""
    p_d_checked = ""
    #Checkar den box som användaren checkade.
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
    return 'API request limit reached. This web application is still under development. We are using an API(application programming interface) to generate results. The API we are utilizing is free and intended for developing purposes. Therefore there is a daily limit to the number of results we are able to request.'


@route("/static/css/<filename>")
def static_files_css(filename):
	'''
	Returnerar statiska filer från mappen "static"
	'''
	return static_file(filename, root="static/css")


@route("/static/img/<filename>")
def static_files_img(filename):
	'''
	Returnerar statiska filer från mappen "img"
	'''
	return static_file(filename, root="static/img")


@route("/static/js/<filename>")
def static_files_js(filename):
	'''
	Returnerar statiska filer från mappen "js"
	'''
	return static_file(filename, root="static/js")


run(host='localhost', port=8080, debug=True)