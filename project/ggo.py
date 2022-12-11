from pprint import pprint
from project.imports_all.project_email import send_email
import os,json
from flask import Blueprint, render_template, url_for, Flask, request, jsonify

from project import app

PATH_CWD = os.path.dirname(os.path.realpath(__file__))

GGO = Blueprint('ggo', __name__,
static_folder=os.path.join(PATH_CWD,"static"),
template_folder=os.path.join(PATH_CWD,"templates"))
@GGO.route('/ggo', methods=['GET','POST'])
def ggo():
    return render_template("ggo.html")

Func_emailAll = Blueprint('func_emailAll', __name__,
static_folder=os.path.join(PATH_CWD,"static"),
template_folder=os.path.join(PATH_CWD,"templates"))
@Func_emailAll.route('/func_emailAll', methods=['GET','POST'])
def func_emailAll():
    dataReply = {'reply':'No emails sent'}
    dataGet = '' if not request.get_json(force=True) else request.get_json(force=True)

    if dataGet['type'] == 'comment':
        try:
            send_email(
            reciever_e=dataGet['recieverEmail'],
            subject=dataGet['subjectEmail'],
            body=dataGet['commentEmail'],
            server_e=dataGet['senderEmail'],
            server_p=dataGet['passwordEmail'], 
            host_addr=dataGet['providerEmail'])
            dataReply['reply'] = 'Comments sent'
        except:
            dataReply['reply'] = 'Comments could not be sent'

    elif dataGet['type'] == 'grades':
        for i in range(dataGet['num']):
            tempBody = f'''
{dataGet['messageEmail']}

Name: {dataGet[str(i)]['name']}         
Assignment Title: {dataGet['assign']}
Assignment Grade: {dataGet[str(i)]['grade']}
Assignment Average: {dataGet['avg']}
'''
            for cat in dataGet[str(i)]["total"]:
                tempBody += f'''
{cat} = {dataGet[str(i)]["cat"][cat]} / {dataGet[str(i)]["total"][cat]}'''
                
            tempBody += f'''\n
Course Grade: {dataGet[str(i)]['current']}
Course Average:'''

            try:
                send_email(
                reciever_e=dataGet[str(i)]['email'],
                subject=dataGet[str(i)]['subject'],
                server_e=dataGet['senderEmail'],
                server_p=dataGet['passwordEmail'], 
                host_addr=dataGet['providerEmail'],
                body= tempBody)
                dataReply['reply'] = 'Grades sent'
            except:
                dataReply['reply'] = 'Grades could not be sent'

    elif dataGet['type'] == 'remind':
        pprint(dataGet['subjectEmail'])
        for i in range(dataGet['num']):
            try:
                send_email(
                reciever_e=dataGet[str(i)]['email'],
                subject=dataGet['subjectEmail'],
                body=dataGet['assign'] + ' is incomplete \n\n'+dataGet['messageEmail'],
                server_e=dataGet['senderEmail'],
                server_p=dataGet['passwordEmail'], 
                host_addr=dataGet['providerEmail'])
                dataReply['reply'] = 'Reminders sent'
            except:
                dataReply['reply'] = 'Reminders could not be sent'
    
    elif dataGet['type'] == 'announce':
        pprint(dataGet)
        for email in dataGet['recieverEmail']:
            try:
                send_email(
                reciever_e=email,
                subject=dataGet['subjectEmail'],
                body=dataGet['messageEmail'],
                server_e=dataGet['senderEmail'],
                server_p=dataGet['passwordEmail'], 
                host_addr=dataGet['providerEmail'])
                dataReply['reply'] = 'Announcement sent'
            except:
                dataReply['reply'] = 'Announcment could not be sent'

    return jsonify(dataReply)