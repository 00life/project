import os
from flask import Blueprint, render_template, url_for, Flask, request

from project import app
from project.imports_all.db import db_give, db_get, limit_cat_size

path_cwd = os.path.dirname(os.path.realpath(__file__))
path_templates = os.path.join(path_cwd,"templates")
path_static = os.path.join(path_cwd,"static")
path_admin = os.path.join(path_static,"data","admin.db")
path_db_ideas = os.path.join(path_static,'data','ideas.db')
verbose = False

Ideas = Blueprint("ideas", __name__, static_folder=path_static, template_folder=path_templates)
@Ideas.route("/ideas", methods=['GET','POST'])
def ideas():
    donate_data = []

    # donate information
    try: 
        temp = db_get(db_name=path_admin, table='donate', cat=['*'], search=['*'])
        try: donate_data = [(title.split()[0], title.split()[1], content, link) for title, content, link, *_ in temp]
        except: donate_data = temp
    except: pass

    # ideas information
    try: 
        temp = db_get(db_name=path_admin, table='ideas', cat=['*'], search=['*'])
        try: ideas_data = [(date[0:8], title, content, link, f'data:image/jpg;base64,{imgBase64_1.decode()}') for title, content, link, imgBase64_1, _, date, *_ in temp]
        except: ideas_data = temp
    except: pass

    # comment information date,pic,content,title
    msg_in = '' if not request.form.get('msg_in') else request.form.get('msg_in')
    
    if msg_in is not '':
        db_give(db_name=path_db_ideas, table='comments', data={'comment':msg_in})
        limit_cat_size(db_name=path_db_ideas, table='comments', cat=['comment'], limit=30)

    try: msg_out = db_get(db_name=path_db_ideas, table='comments', cat=['comment'], search=['*'])
    except: msg_out = [['','','','']]

    if verbose: print(  '\033[32m[*] msg_in:\033[0m', msg_in,
                '\n',   '\033[31m[*] msg_in:\033[0m', msg_out)
    
    return render_template("ideas.html", msg_out=msg_out, donate_data=donate_data, ideas_data=ideas_data)

if __name__ == "__main__":
    app.run(debug=True)