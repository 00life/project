import os
from flask import Blueprint, render_template, url_for, flash, request, Flask,session

from project import app
from project.imports_all.project_email import send_email

path_cwd = os.path.dirname(os.path.realpath(__file__))
path_templates = os.path.join(path_cwd,'templates')
path_static = os.path.join(path_cwd,'static')
path_admin = os.path.join(path_static,"data","class.db")
errors = []
VERBOSE = False
colr = {'0':1,'1':2,'2':3,'3':4,'4':5,'5':6,'6':1,'7':2,'8':3,'9':4}

CM = Blueprint('cm', __name__, static_folder=path_static, template_folder=path_templates)
@CM.route('/cm', methods=['GET','POST'])
def cm():
    teacher = ''        if not request.form.get('teacher') else request.form.get('teacher')
    class_code = ''     if not request.form.get('class_code') else request.form.get('class_code')
    date_today = None   if not request.form.get('date_today') else request.form.get('date_today')
    start_time = None   if not request.form.get('start_time') else request.form.get('start_time')
    end_time = None     if not request.form.get('end_time') else request.form.get('end_time')
    names = None        if not request.form.get('names') else request.form.get('names')
    name_list = ''      if not names else [" ".join(name.split()) for name in names.split('\n')]
    hddn_notes_list = ''    if not request.form.get('hddn_notes_list') else request.form.get('hddn_notes_list')
    hddn_pass_list = ''     if not request.form.get('hddn_pass_list') else request.form.get('hddn_pass_list')
    hddn_attn_list = ''     if not request.form.get('hddn_attn_list') else request.form.get('hddn_attn_list')
    input_custom = ''       if not request.form.get('input_custom') else request.form.get('input_custom')
    alert_start = 14        if not request.form.get('alert_start') else request.form.get('alert_start')  
    alert_end = 15          if not request.form.get('alert_end') else request.form.get('alert_end')
    email_report = 'off'    if not request.form.get('email_report') else request.form.get('email_report')
    hddn_report = ''        if not request.form.get('hddn_report') else request.form.get('hddn_report')
    from_email = ''         if not request.form.get('from_email') else request.form.get('from_email')
    to_email = ''           if not request.form.get('to_email') else request.form.get('to_email')
    epwd = ''               if not request.form.get('epwd') else request.form.get('epwd')
    eprovide = ''           if not request.form.get('eprovide') else request.form.get('eprovide')
    subject = ''            if not request.form.get('subject') else request.form.get('subject')
    hddn_all_check = 'off'  if not request.form.get('hddn_all_check') else request.form.get('hddn_all_check')
    hddn_check_std = 'off'  if not request.form.get('hddn_check_std') else request.form.get('hddn_check_std')
    hddn_std = ''           if not request.form.get('hddn_std') else request.form.get('hddn_std')
        
    if email_report == 'on':
        try: send_email(reciever_e=to_email, subject=subject, body=hddn_report, server_e=from_email, server_p=epwd, host_addr=eprovide)
        except: errors.append('[!!] cm.py cm Error 1.')
    
    if VERBOSE: 
        output_console = {'teacher:':teacher, 'class_code:': class_code,'date_today:':date_today, 'start_time:':start_time,
                        'end_time:':end_time, 'alert_start:':alert_start,'alert_end:':alert_end,'email_report:':email_report,
                        'from_email:':from_email,'to_email:':to_email,'subject:':subject,'epwd:':epwd,'eprovide:':eprovide,       
                        'name_list:':name_list,'hddn_report:':hddn_report, 'hddn_std:':hddn_std}
        for i, var in enumerate(output_console): print(f'\033[3{colr[str(i%10)]}m[*]',var,'\033[0m',output_console[var])

    return render_template('cm.html', names=names, name_list=name_list, teacher=teacher, class_code=class_code, date_today=date_today,
                            start_time=start_time, end_time=end_time,hddn_notes_list=hddn_notes_list, hddn_pass_list=hddn_pass_list, 
                            hddn_attn_list=hddn_attn_list, input_custom=input_custom,alert_start=alert_start,alert_end=alert_end,
                            hddn_report=hddn_report,from_email=from_email, to_email=to_email, email_report=email_report,
                            eprovide=eprovide, epwd=epwd, subject=subject, hddn_all_check=hddn_all_check, hddn_check_std=hddn_check_std, 
                            hddn_std=hddn_std)

if __name__ == "__main__":
    app.run(debug=True)