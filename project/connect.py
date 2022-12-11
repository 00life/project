import os, json, time
from flask import Blueprint, render_template, request, url_for, Flask, jsonify

from project import app
from project.imports_all.db import db_give, db_get, db_deleteTable, db_update, db_tableNames

path_cwd = os.path.dirname(os.path.realpath(__file__))
path_template = os.path.join(path_cwd,"templates")
path_static = os.path.join(path_cwd,"static")
path_admin = os.path.join(path_static,"data","admin.db")
path_class = os.path.join(path_static,"data","class.db")
VERBOSE = False
COLR = {'0':1,'1':2,'2':3,'3':4,'4':5,'5':6,'6':1,'7':2,'8':3,'9':4}
errors = []

DropMenu = Blueprint('dropmenu', __name__, static_folder=path_static, template_folder=path_template)
@DropMenu.route('/dropmenu', methods=['GET','POST'])
def dropmenu():
    dataReply = {}
    dataGet = '' if not request.get_json(force=True) else request.get_json(force=True)

    if dataGet['list'] == 'true':
        try: 
            temp = db_get(db_name=path_admin, table='ideas', cat=['*'], search=['*'])
            dataReply['ideasList'] = [(title,link) for title, _, link, *_ in temp]
        except Exception as e: errors.append(f'connect.py dropmenu Error 1 {e}')
        try: 
            temp = db_get(db_name=path_admin, table='apps', cat=['*'], search=['*'])
            dataReply['appsList'] = [(title,link) for title, _, link, *_ in temp] 
        except Exception as e: errors.append(f'connect.py dropmenu Error 2 {e}')
        try: 
            temp = db_get(db_name=path_admin, table='donate', cat=['*'], search=['*'])
            dataReply['donateList'] = [(title.split()[1],link) for title, _, link, *_ in temp]
        except Exception as e: errors.append(f'connect.py dropmenu Error 3 {e}')
    
    if VERBOSE and len(errors) > 0: print('\033[41m[!!]',errors,'\033[0m')
    return jsonify(dataReply)

CreateSTD_func = Blueprint('createSTD_func',__name__, static_folder=path_static, template_folder=path_template)
@CreateSTD_func.route('/createSTD_func', methods=['GET','POST'])
def createSTD_func():
    DELETE_TABLE_TIME_SEC = 43200
    dataReply = {}
    dataGet = '' if not request.get_json(force=True) else request.get_json(force=True)

    if dataGet['key'] == 'makeClass':
        try: 
            db_give(db_name=path_class, table=dataGet['classNum'], data={
            'out':dataGet['out'],
            'ready':dataGet['ready'],
            'waiting':dataGet['waiting'],
            'present':dataGet['present'],
            'allowNum':int(dataGet['allowNum']),
            'students':list(dataGet['pwdStudent'].keys()),
            'passwords':list(dataGet['pwdStudent'].values()),
            'classCode':dataGet['classCode'],
            'teacher':dataGet['teacher'],
            'pwdEnabled':dataGet['pwdEnabled'],
            'readyWait':dataGet['readyWait']
            })

            classes = db_tableNames(db_name=path_class)
            for clss in classes:
                temp = db_get(db_name=path_class, table=clss, cat=['*'], search=['*'])
                if float(float(time.time()) - float(temp[0][-2])) > float(DELETE_TABLE_TIME_SEC):
                    db_deleteTable(db_name=path_class, table=clss)

        except Exception as e: errors.append(f'connect.py createSTD_func Error 1 {e}')
        dataReply['reply'] = dataGet['classNum'] + ' STD Class Created'

    elif dataGet['key'] == 'delClass':
        try: db_deleteTable(db_name=path_class, table=dataGet['classNum'])
        except Exception as e: errors.append(f'connect.py createSTD_func Error 2 {e}')
        dataReply['reply'] = dataGet['classNum'] +' STD Class Deleted'

    if VERBOSE and len(errors) > 0: print('\033[41m',errors,'\033[0m')
    return jsonify(dataReply)

XmlSTD_func = Blueprint('xmlSTD_func', __name__, static_folder=path_static, template_folder=path_template)
@XmlSTD_func.route('/xmlSTD_func', methods=['GET','POST'])
def xmlSTD_func():
    dataReply, ready, present = {}, [], []
    dataGet = '' if not request.get_json(force=True) else request.get_json(force=True)
    waiting = [] if not dataGet['waiting'] else dataGet['waiting']
    out = [] if not dataGet['out'] else dataGet['out']
    back = [] if not dataGet['back'] else dataGet['back']

    if dataGet['key'] == 'xmlSTD_func':
        try: 
            temp = db_get(db_name=path_class, table=dataGet['classNum'], cat=['id'], search=[1])
            db_out, db_ready, db_waiting, _, db_allowNum, db_students,*_ = temp[0]

            for student in json.loads(db_out):
                if student not in out: out.append(student)
            for student in json.loads(db_ready):
                if student not in ready: ready.append(student)
            for student in json.loads(db_waiting):
                if student not in waiting: waiting.append(student)
            
            for student in back:
                if student in out: out.remove(student)
                if student in ready: ready.remove(student)
                if student in waiting: waiting.remove(student)
            for student in out:
                if student in ready: ready.remove(student)
                if student in waiting: waiting.remove(student)
            for student in ready:
                if student in waiting: waiting.remove(student)
            
            present = [student for student in json.loads(db_students)]
            for student in json.loads(db_students):
                if student in out: present.remove(student)
                if student in ready: present.remove(student)
                if student in waiting: present.remove(student)
            
            while len(out)+len(ready) < db_allowNum and len(waiting) > 0: ready.append(waiting.pop(0))
            dataReply = {'waiting': waiting, 'ready':ready, 'out':out, 'present':present}
            db_update(db_name=path_class, table=dataGet['classNum'], data=dataReply, cat=['id'], search=[1])
        except Exception as e: errors.append(f'connect.py xmlSTD_func Error 1 {e}')

    if VERBOSE: 
        output_console = {'xmlSTD waiting':waiting, 'xmlSTD ready':ready, 'xmlSTD out':out, 'xmlSTD table':dataGet['classNum']}
        for i, var in enumerate(output_console): print(f'\033[3{COLR[str(i%10)]}m[*]',var,'\033[0m',output_console[var])

    if VERBOSE and len(errors) > 0: print('\033[41m[!!]',errors,'\033[0m')
    return jsonify(dataReply)

XmlCM_func = Blueprint('xmlCM_func', __name__, static_folder=path_static, template_folder=path_template)
@XmlCM_func.route('/xmlCM_func', methods=['GET','POST'])
def xmlCM_func():
    dataReply, waiting, ready, out, present, pwdEnabled = {},[],[],[],[],1
    dataGet = '' if not request.get_json(force=True) else request.get_json(force=True)
    
    if dataGet['key'] == 'Update_CM':
        try: 
            temp = db_get(db_name=path_class, table=dataGet['classNum'], cat=['id'], search=[1])
            out = json.loads(temp[0][0])
            ready = json.loads(temp[0][1])
            waiting = json.loads(temp[0][2])
            students = json.loads(temp[0][5])
            passwords = json.loads(temp[0][6])
            pwdEnabled = temp[0][9]
            present = [student for student in students]
            for student in students:
                if student in out: present.remove(student)
                if student in ready: present.remove(student)
                if student in waiting: present.remove(student)
        except Exception as e: errors.append(f'connect.py xmlCM_func Error 1 {e}') 
        dataReply = {'waiting': waiting,    'ready':ready, 'out':out,   'present':present,
                    'passwords':passwords,  'pwdEnabled':pwdEnabled}
    
    elif dataGet['key'] == 'Update_STD':
        try:
            dataUpdate = {'out':dataGet['out'], 'present':dataGet['present'], 'allowNum':dataGet['allowNum'],
                        'pwdEnabled':dataGet['pwdEnabled'], 'readyWait':dataGet['readyWait']}
            db_update(db_name=path_class, table=dataGet['classNum'], data=dataUpdate, cat=['id'], search=[1])
        except Exception as e: errors.append(f'connect.py xmlCM_func Error 2 {e}')      

    if VERBOSE:
        output_console = {'xmlCM waiting':waiting, 'xmlCM ready':ready, 'xmlCM out':out, 'xmlCM present':present, 'xmlCM table':dataGet['classNum']}
        for i, var in enumerate(output_console): print(f'\033[3{COLR[str(i%10)]}m[*]',var,'\033[0m',output_console[var])

    if VERBOSE and len(errors) > 0: print('\033[41m[!!]',errors,'\033[0m')
    return jsonify(dataReply)

ShowSTD_func = Blueprint('showSTD_func', __name__, static_folder=path_static, template_folder=path_template)
@ShowSTD_func.route('/showSTD_func', methods=['GET','POST'])
def showSTD_func():
    dataReply = {}
    dataGet = '' if not request.get_json(force=True) else request.get_json(force=True)

    if dataGet['key'] == 'showSTD_func':
        try:
            temp = db_get(db_name=path_class, table=dataGet['classNum'], cat=['id'], search=[1])
            dataReply = {'students':json.loads(temp[0][5]),'passwords':json.loads(temp[0][6]),'pwdEnabled':temp[0][9]}
        except Exception as e: errors.append(f'connecty.py showSTD Error 1 {e}')

    if VERBOSE:
        output_console = {  'ShowSTD students':dataReply['students'],
                            'ShowSTD passwords':dataReply['passwords'],
                            'ShowSTD pwdEnabled':dataReply['pwdEnabled']}
        for i, var in enumerate(output_console): print(f'\033[3{COLR[str(i%10)]}m[*]',var,'\033[0m',output_console[var])

    if VERBOSE and len(errors) > 0: print('\033[41m[!!]',errors,'\033[0m')
    return jsonify(dataReply)

if __name__ == "__main__":
    app.run(debug=True)