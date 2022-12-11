import os
from flask import Blueprint, render_template, url_for, Flask, request

from project import app
from project.imports_all.db import db_give, db_get, db_deleteRow, db_tableNames, db_deleteTable

path_cwd = os.path.dirname(os.path.realpath(__file__))
path_templates = os.path.join(path_cwd,"templates")
path_static = os.path.join(path_cwd,"static")
path_admin = os.path.join(path_static,"data","admin.db")
path_imgDFLT = os.path.join(path_static,'img','default.gif')
verbose = True

Admin = Blueprint('admin', __name__, static_folder=path_static, template_folder=path_templates)
@Admin.route('/admin', methods=['GET','POST'])
def admin():

    add = ''        if not request.form.get('add') else request.form.get('add')
    delete = ''     if not request.form.get('del') else request.form.get('del')
    del_spec = ''   if not request.form.get('del_spec') else request.form.get('del_spec')
    radio = ''      if not request.form.get('radio') else request.form.get('radio')
    title = ''      if not request.form.get('title') else request.form.get('title')
    content = ''    if not request.form.get('content') else request.form.get('content')
    link = ''       if not request.form.get('link') else request.form.get('link')
    img_path1 = path_imgDFLT  if not request.form.get('show_path1') else request.form.get('show_path1')
    img_path2 = path_imgDFLT  if not request.form.get('show_path2') else request.form.get('show_path2')
    tabNames = []    if not db_tableNames(db_name=path_admin) else db_tableNames(db_name=path_admin)
    databases = [item for item in os.listdir(os.path.dirname(path_admin)) if item.endswith('.db')]
    
    # adding and deleting data to the admin.db
    if add == 'ADD':
        try: db_give(db_name=path_admin, table=radio, data={'title':title,'content': content,'link':link, 'image1':img_path1,'image2':img_path2})
        except: db_give(db_name=path_admin, table=radio, data={'title':title,'content': content,'link':link, 'image1':path_imgDFLT,'image2':path_imgDFLT})
    elif add == '' and delete != '':
        del_table = [(int(ids),'id') for ids in delete.split(',')]
        ids, cat = zip(*del_table) 
        try: db_deleteRow(db_name=path_admin, table=radio, cat=cat, search=ids)
        except: pass
    elif add == '' and (del_spec in tabNames):
        try: db_deleteTable(db_name=path_admin, table=del_spec)
        except: pass
    elif add == '' and (del_spec not in tabNames) and (del_spec.endswith('.db')):
        try:
            path_db = os.path.join(os.path.dirname(path_admin),del_spec)
            if os.path.exists(path_db):
                os.remove(path_db)
        except: pass
    else: pass

    # Retrieving data from admin.db for the admin page
    data = {'home':[],'apps':[],'ideas':[],'donate':[],'contact':[]}
    for page in data:
        try:
            temp = db_get(db_name=path_admin, table=page, cat=['*'], search=['*'])
            try: data[page] = [(idNum, date, title, content, link,'data:image/png;base64,'+imgBase64_1.decode(), 'data:image/png;base64,'+imgBase64_2.decode()) for title, content, link, imgBase64_1, imgBase64_2, date, _, idNum in temp]
            except: data[page] = temp
        except: pass

    # Printing incoming data
    if verbose: print(  '\033[31m[+] add:\033[0m',add,         '\033[36m[-] delete:\033[0m',delete, '\033[32m[*] title:\033[0m',title,
                        '\033[32m[*] content:\033[0m',content, '\033[31m[*] radio:\033[0m',radio,   '\033[33m[*] tabName:\033[0m',tabNames,
                        '\033[33m[*] del_spec:\033[0m',del_spec,
                '\n',   '\033[34m[*] img_path1:\033[0m',img_path1,
                '\n',   '\033[35m[*] img_path2:\033[0m', img_path2)
    
    return render_template("admin.html",    home_data=data['home'],     apps_data=data['apps'],         ideas_data=data['ideas'],
                                            donate_data=data['donate'], contact_data=data['contact'],   radio=radio,
                                            tabNames=tabNames, pages=data.keys(), databases=databases)

if __name__ == "__main__":
    app.run(debug=True)