import os
from flask import Blueprint, render_template, url_for, Flask

from project import app
from project.imports_all.db import db_get

path_cwd = os.path.dirname(os.path.realpath(__file__))
path_templates = os.path.join(path_cwd,"templates")
path_static = os.path.join(path_cwd,"static")
path_admin = os.path.join(path_static,"data","admin.db")

Home = Blueprint("home", __name__, static_folder=path_static, template_folder=path_templates)
@Home.route("/home", methods=['GET','POST'])
@Home.route("/", methods=['GET','POST'])
def home():
    donate_data, home_data = [], []

    # donate information
    try: 
        temp = db_get(db_name=path_admin, table='donate', cat=['*'], search=['*'])
        try: donate_data = [(title.split()[0], title.split()[1], content, link) for title, content, link, *_ in temp]
        except: donate_data = temp
    except: pass

    # announcment information
    try: 
        temp = db_get(db_name=path_admin, table='home', cat=['*'], search=['*'])
        try: home_data = [(date[0:8], title, content, link ,f'data:image/jpg;base64,{imgBase64_1.decode()}') for title, content, link, imgBase64_1, _, date, *_ in temp]
        except: home_data = temp
    except: pass
 

    return render_template("home.html", donate_data=donate_data, home_data=home_data)

if __name__ == "__main__":
    app.run(debug=True)