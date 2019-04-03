#   ====================================
#
#   Kodhistorik
#   
#   ------------------------------------
#   [det man gjort] -[yymmdd] -[namn/id]
#   ====================================
#
#   ====================================
#   -   -   -   -   -   -   -   -   -
#   Initial Commit V.1 -190403 -olta
#   -   -   -   -   -   -   -   -   -



#   ====================================
#   Imports
from bottle import route, run, template, request, get, static_file
from random import choice
import json



#   ====================================
#   globals
load_file = "links.json"



def get_file():
    '''
    Hämtar lexikonen från json-filen med alla länkar, dess protein och ID:n. Finns inte filen skapas en ny tom.
    '''
    try:
        my_file = open(load_file, "r")
        links = json.loads(my_file.read())
        my_file.close()
        return links
    except:
        my_file = open(load_file, "w")
        links = []
        my_file.write(json.dumps(links))
        return links

@route('/')
@route('/index/')
def index_page():
    '''
    Retunerar index.html med tomma placeholders.
    '''
    return template("index", placeholder_link="", placeholder_used_ids="", placeholder_hidden="hidden", p_m_checked="", p_b_checked="", p_s_checked="", p_v_checked="", p_d_checked="")

@route('/generate/',method='POST')
def generate_recipe():
    '''
    Genererar en slumpmässigt länk utifrån valet av protein.
    '''
    used_ids = request.forms.get('used_ids')
    choosen_protein = request.forms.get('protein')
    links = get_file()
    links_updated = []

    #Hämtar alla redan genererade ID:n. Lägger till alla länkar från links som inte genererats tidigare i links_updated. Är used_ids tom läggs alla länkar till.
    if used_ids != "":
        used_ids_list = used_ids[1:].split(",")
        used_ids_list = [int(i) for i in used_ids_list]
        for link in links:
            if link["id"] not in used_ids_list:
                links_updated.append(link)
    else:
        links_updated = links
    links_updated_2 = []
    
    #Sorterar ut alla med det valda proteinet och lägger de i links_updated_2.
    for link in links_updated:
        if link["protein"] == choosen_protein or choosen_protein == "dont_know":
            links_updated_2.append(link)
    #Om det är slut på länkar retuneras index.html med alla placeholders tomma. Tillfällig lösning för att programmet inte ska krascha.
    if links_updated_2 == []:
        return template("index", placeholder_used_ids="", placeholder_link="", placeholder_hidden="hidden", p_m_checked="", p_b_checked="", p_s_checked="", p_v_checked="", p_d_checked="")
    else:
        #Slumpar fram ett lexikon från links_updated_2 och retunerar dess länk till användaren genom index.html.
        random_link = choice(links_updated_2)
        used_ids += "," + str(random_link["id"])
        return_link = random_link["link"]
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
        return template("index", placeholder_used_ids=used_ids, placeholder_link=return_link, placeholder_hidden="", p_m_checked=p_m_checked, p_b_checked=p_b_checked, p_s_checked=p_s_checked, p_v_checked=p_v_checked, p_d_checked=p_d_checked)

@route("/static/<file_name>")
def static_files(file_name):
	'''
	Returnerar statiska filer från mappen "static"
	'''
	# Returnerar den efterfrågade filen
	return static_file(file_name, root="static")

run(host='localhost', port=8080, debug=True)