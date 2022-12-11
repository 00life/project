import os, json
from flask import Blueprint, render_template, url_for, Flask, request,jsonify

from project import app
from project.imports_all.db import db_get

path_cwd = os.path.dirname(os.path.realpath(__file__))
path_templates = os.path.join(path_cwd,"templates")
path_static = os.path.join(path_cwd,"static")
path_class = os.path.join(path_static,"data","class.db")
errors = []
VERBOSE = False
colr = {'0':1,'1':2,'2':3,'3':4,'4':5,'5':6,'6':1,'7':2,'8':3,'9':4}

Std = Blueprint('std', __name__, static_folder=path_static, template_folder=path_templates)
@Std.route('/std', methods=['GET','POST'])
def std():
    teacher, students, passwords, classCode, pwdEnabled, readyWait = '',[],[],'',[],999
    classNum = '' if not request.form.get('send') else request.form.get('send')

    try: 
        temp = db_get(db_name=path_class, table=classNum, cat=['id'], search=[1])
        students = json.loads(temp[0][5])
        passwords = json.loads(temp[0][6])
        classCode = temp[0][7]
        teacher = temp[0][8]
        pwdEnabled = temp[0][9]
        readyWait = temp[0][10]
    except Exception as e: errors.append(f'std.py Error 1 {e}')
    
    if VERBOSE: 
        output_console = {'Std teacher':teacher, 'Std students':students, 'Std classCode':classCode, 'Std passwords':passwords}
        for i, var in enumerate(output_console): print(f'\033[3{colr[str(i%10)]}m[*]',var,'\033[0m',output_console[var])

    if VERBOSE and len(errors) > 0: print('\033[41m[!!]',errors,'\033[0m')
    return render_template("std.html",  classNum=classNum,      teacher=teacher,        students=students, 
                                        passwords=passwords,    classCode=classCode,    pwdEnabled=pwdEnabled,
                                        readyWait=readyWait)

if __name__ == "__main__":
    app.run(debug=True)