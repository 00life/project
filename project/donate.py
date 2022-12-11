import os
from flask import Blueprint, render_template, url_for, Flask

from project import app
from project.imports_all.db import db_get

path_cwd = os.path.dirname(os.path.realpath(__file__))
path_templates = os.path.join(path_cwd,"templates")
path_static = os.path.join(path_cwd,"static")
path_admin = os.path.join(path_static,"data","admin.db")

Donate = Blueprint("donate", __name__, static_folder=path_static, template_folder=path_templates)
@Donate.route("/donate", methods=['GET','POST'])
def donate():
    new_donate_data = []

    # donate information
    try: 
        donate_data = db_get(db_name=path_admin, table='donate', cat=['*'], search=['*'])
        try: new_donate_data = [(title, content, link, 'data:image/png;base64,'+imgBase64_1.decode(),'data:image/png;base64,'+imgBase64_2.decode()) for title, content, link, imgBase64_1, imgBase64_2, *_ in donate_data]
        except: new_donate_data = donate_data
    except: pass

    # payment information

    path_pay = os.path.join(path_static,'text_data','pay.txt')
    with open(path_pay,'r') as fout:
        data_list = fout.read().split('\n')

    pay_info = []
    for data in data_list:
        abbr, title, link, num = data.split()
        pic = abbr[0:-1]+".png"
        pay_info.append((pic, abbr, title, link, num.replace(' ','_')))

    return render_template("donate.html",pay_info=pay_info, new_donate_data=new_donate_data)

if __name__ == "__main__":
    app.run(debug=True)