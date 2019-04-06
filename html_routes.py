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
    return template("index", placeholder_link="", placeholder_img="", placeholder_used_ids="", placeholder_hidden="hidden", p_m_checked="", p_b_checked="", p_s_checked="", p_v_checked="", p_d_checked="")


@route('/generate/',method='POST')
def generate_recipe():
    '''
    Genererar en slumpmässigt länk utifrån valet av protein.
    '''
    used_ids = request.forms.get('used_ids')
    choosen_protein = request.forms.get('protein')
    
    used_ids_list = []
    if used_ids != "":
        used_ids_list = used_ids[1:].split(",")

    while True:
        return_recipe = ReqAPI.generate_link(choosen_protein)
        if return_recipe['recipe_id'] not in used_ids_list:
            used_ids += "," + return_recipe['recipe_id']
            break
    
    return return_template(choosen_protein, return_recipe, used_ids)


def return_template(choosen_protein, return_recipe, used_ids):
    p_m_checked = ""
    p_b_checked = ""
    p_s_checked = ""
    p_v_checked = ""
    p_d_checked = ""
    #Checkar den box som användaren checkade.
    if choosen_protein == "meat":
        p_m_checked = "checked"
    elif choosen_protein == "bird":
        p_b_checked = "checked"
    elif choosen_protein == "sea":
        p_s_checked = "checked"
    elif choosen_protein == "veg":
        p_v_checked = "checked"
    elif choosen_protein == "dont_know":
        p_d_checked = "checked"
    return template("index", placeholder_used_ids=used_ids, placeholder_link=return_recipe["source_url"], placeholder_img=return_recipe["image_url"], placeholder_hidden="", p_m_checked=p_m_checked, p_b_checked=p_b_checked, p_s_checked=p_s_checked, p_v_checked=p_v_checked, p_d_checked=p_d_checked)


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