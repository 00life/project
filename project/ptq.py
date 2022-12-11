import os, time
from flask import render_template, url_for, flash, request, Flask, Blueprint

from project import app
from project.imports_ptq.chemistry import chem_quest, evaluate
from project.imports_ptq.conditions import cond
from project.imports_all.project_email import send_email

path_cwd =          os.path.dirname(os.path.realpath(__file__))
path_templates =    os.path.join(path_cwd,"templates")
path_static =       os.path.join(path_cwd,"static")
verbose = False

DV_as = 1       ;       DV_un = 'Reza T'
DV_ae = 36      ;       DV_em = 'reza@genius.com'
DV_nq = 0       ;       DV_gr = 0

PTQ = Blueprint("ptq", __name__, static_folder=path_static, template_folder=path_templates)
@PTQ.route("/ptq", methods=['GET','POST'])

def ptq():

    atomic_start = DV_as    if not request.form.get('atomic_start') else request.form.get('atomic_start')
    atomic_end = DV_ae      if not request.form.get('atomic_end') else request.form.get('atomic_end')
    num_ques = DV_nq        if not request.form.get('questions') else request.form.get('questions')
    username = DV_un        if not request.form.get('username') else request.form.get('username')
    email = DV_em           if not request.form.get('email') else request.form.get('email')
    group = DV_gr           if not request.form.get('group') else request.form.get('group')
    delay = ""              if group == 0 else str(group)[-1:] + "h"
    start_reset = False     if not request.form.get('start_reset') else True
    end_time = False        if not request.form.get('end_time') else True
    time_in =               round(time.time())
    time_out = 0            if not request.form.get('time_out') else request.form.get('time_out')
    time_diff =             abs(int(time_out)-int(time_in))
    elapse_time = ''        if time_out == 0 else f"{round(time_diff/3600)} hr {round(time_diff/60)} min {round(time_diff)} s"

    con = cond(int(atomic_start),int(atomic_end),int(num_ques))
    
    if (True,'') not in con:
        boolean, msg = {boolean for boolean,_ in con}, {msg for _,msg in con}
        {flash(message) for message in msg}
        
        return render_template("ptq.html",  DV_as=DV_as,    DV_ae=DV_ae,    DV_nq=DV_nq,
                                            DV_un=DV_un,    DV_em=DV_em,    DV_gr=DV_gr)
    if verbose: 
        print(  '\n',
                '\033[32m[+]\033[0m atomic_start:',atomic_start,
                '\033[31m[+]\033[0m atomic_end:',atomic_end,
                '\033[33m[+]\033[0m num_questions:',num_ques,
                '\033[33m[!!] start_reset:\033[0m',start_reset,
                '\033[34m[!!] username:\033[0m',username,
                '\033[35m[!!] email:\033[0m',email,
                '\033[36m[!!] group:\033[0m',group,'\n',
                '\033[90m[!!] end_time:\033[0m',end_time,
                '\033[92m[+] time_in:\033[0m',time_in,
                '\033[91m[+] time_out:\033[0m',time_out,
                '\033[93m[!!] time_diff:\033[0m',time_diff,
                '\033[94m[!!] elapse_time:\033[0m',elapse_time)
    
    N = []  if not request.form.getlist('N') else request.form.getlist('N')
    Q = []  if not request.form.getlist('Q') else request.form.getlist('Q')
    A = []  if not request.form.getlist('A') else request.form.getlist('A')
    G = []  if not request.form.getlist('G') else request.form.getlist('G')

    input_ans = []              if not request.form.getlist('input_ans') else request.form.getlist('input_ans')
    (results,score) = ([],[])   if not end_time else evaluate(get_ans=input_ans, ques=Q, ans=A, given=G, num=N)
    chem_ques = []              if not start_reset else chem_quest(int(atomic_start),int(atomic_end),int(num_ques))
    
    if verbose: 
        print(  '\n',
                '\033[33m[!!] chem_ques:\033[0m',chem_ques,'\n',
                '\033[33m[!!] input_ans:\033[0m',input_ans,'\n',
                '\033[33m[!!] results:\033[0m',results,'\n',
                '\033[33m[!!] Score:\033[0m',score,'\n',)

    if email != DV_em:
        send_email( reciever_e=email, subject="PTQ Results for "+username+" "+str(score), 
        body='\n'.join(results), server_e="pawn88@live.com",server_p="Westside99", host_addr='hotmail')

    return render_template("ptq.html",  chem_ques=chem_ques,    score=score,        results=results,    delay=delay,
                                        end_time=end_time,      time_in=time_in,    elapse_time=elapse_time,
                                        DV_as=DV_as,    DV_ae=DV_ae,    DV_nq=DV_nq,
                                        DV_un=DV_un,    DV_em=DV_em,    DV_gr=DV_gr)
   
        
    
    # con = cond(atomic_start, atomic_end, num_questions)
    # boolean, msg = {boolean for boolean,_ in con}, {msg for _,msg in con}
    # if False in boolean:
    #     {flash(message) for message in msg}
    #     return render_template("ptq.html", form=form)
    
    # if form.validate_on_submit():
    #     flash(f'{username}"\'s" quiz will be submitted to {email} {delay}')

if __name__ == "__main__":
    app.run(debug=True)
