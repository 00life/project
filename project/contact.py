import os
from flask import Blueprint, render_template, url_for, Flask

from project import app
from project.imports_all.db import db_get

path_cwd = os.path.dirname(os.path.realpath(__file__))
path_templates = os.path.join(path_cwd,"templates")
path_static = os.path.join(path_cwd,"static")
path_admin = os.path.join(path_static,"data","admin.db")

Contact = Blueprint('contact', __name__, static_folder=path_static, template_folder=path_templates)
@Contact.route('/contact', methods=['GET','POST'])
def contact():
    donate_data, contact_data = [],[]

    # donate information
    try: 
        temp = db_get(db_name=path_admin, table='donate', cat=['*'], search=['*'])
        try: donate_data = [(title.split()[0], title.split()[1], content, link) for title, content, link, *_ in temp]
        except: donate_data = temp
    except: pass

    # contact information
    try: 
        temp = db_get(db_name=path_admin, table='contact', cat=['*'], search=['*'])
        try: contact_data = [(title, content, link) for title, content, link, *_ in temp]
        except: contact_data = temp
    except: pass

    return render_template("contact.html", donate_data=donate_data, contact_data=contact_data)

if __name__ == "__main__":
    app.run(debug=True)