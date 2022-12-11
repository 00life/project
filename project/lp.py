import os
from project import app
from flask import Blueprint, render_template, url_for, flash, request
from project.imports_lp.list_parser import evaluate, line_by_line

current_dir =       os.path.dirname(os.path.realpath(__file__))
templates_path =    os.path.join(current_dir,'templates')
static_path =       os.path.join(current_dir,'static')
verbose =           False

LP = Blueprint('lp', __name__, static_folder=static_path, template_folder=templates_path)
@LP.route('/lp', methods=['GET','POST'])
def lp():
    start_target = '\\'     if not request.form.get('st') else request.form.get('st')
    start_post_space = 0    if not request.form.get('sps') else request.form.get('sps')
    start_post_enter = 0    if not request.form.get('spe') else request.form.get('spe')
    end_target = '\\\\'     if not request.form.get('et') else request.form.get('et')
    end_post_space = 0      if not request.form.get('eps') else request.form.get('eps')
    end_post_enter = 0      if not request.form.get('epe') else request.form.get('epe')
    cal_start = 0           if not request.form.get('cal_start') else request.form.get('cal_start')
    cal_end = 0             if not request.form.get('cal_end') else request.form.get('cal_end')
    input_text = ""         if not request.form.get('input_text') else request.form.get('input_text')
    input_parse_all = False if not request.form.get('input_parse_all') else True
    input_parse_next = False if not request.form.get('input_parse_next') else True
    lbl_checkbox = False    if not request.form.get('lbl_checkbox') else True
    next_count = 0          if not request.form.get('next_count') else request.form.get('next_count')
    list_act = ""           if not request.form.get('list_act') else request.form.get('list_act')
    output_text, next_limit, count = "", "", ""
    
    if verbose:
        print('\033[32m [!] start_target:\033[0m', start_target,'\033[31m [!] end_target:\033[0m',end_target)
        print('\033[32m [!] start_post_space:\033[0m',start_post_space,'\033[31m [!] end_post_space:\033[0m',end_post_space)
        print('\033[32m [!] start_post_enter:\033[0m',start_post_enter,'\033[31m [!] end_post_enter:\033[0m',end_post_enter)
    
    if lbl_checkbox is False:
        try:    import_results = evaluate(  start_tgt=str(start_target),    sps=int(start_post_space),  spe=int(start_post_enter),
                                            end_tgt=str(end_target),        eps=int(end_post_space),    epe=int(end_post_enter),
                                            text=str(input_text),           cal_s=int(cal_start),       cal_e=int(cal_end)  )
        except: flash('Something went Wrong...')

        if input_parse_all is True:
            try: 
                output_text = list(import_results)
                if list_act == "":
                    output_text = [f'{text}' for text in output_text]
                    output_text = '\n'.join(output_text)
                elif list_act == "number":
                    output_text = [f'{i+1}. {text}' for i, text in enumerate(output_text)]
                    output_text = '\n'.join(output_text)
                elif list_act == "∙ ":
                    output_text = [f'∙ {text}' for text in output_text]
                    output_text = '\n'.join(output_text)

                count = output_text.count('\n') + 1
            except: flash('Something went Wrong...')

        elif input_parse_next is True:
            try:
                results = []
                for i in range(int(next_count)):
                    if list_act == "number":
                        try: results.append(f"{i+1}. " + next(import_results))
                        except: next_limit = 'limit'
                    else:
                        try: results.append(list_act+next(import_results))
                        except: next_limit = 'limit'
                output_text = results
                output_text = '\n'.join(output_text)
                count = output_text.count('\n') + 1
            except: flash('Something went Wrong...')
    
    elif lbl_checkbox is True:
        try:    import_lbl = line_by_line(  start_tgt=str(start_target),    sps=int(start_post_space),  spe=int(start_post_enter),
                                            end_tgt=str(end_target),        eps=int(end_post_space),    epe=int(end_post_enter),
                                            split_text=str(input_text),     cal_s=int(cal_start),       cal_e=int(cal_end)  )
        except: flash('Something went Wrong...')

        if input_parse_all is True:
            try:
                generator_results = list(import_lbl)
                output_text = [item for results in generator_results for item in results]

                if list_act == "number":
                    output_text = [f'{i+1}. {item}' for i, item in enumerate(output_text)]
                    output_text = '\n'.join(output_text)
                else:
                    output_text = [f'{list_act}{item}' for item in output_text]
                    output_text = '\n'.join(output_text)

                count = output_text.count('\n') + 1    
            except: flash('Something went Wrong...')

        elif input_parse_next is True:
            try:
                results = []
                for _ in range(int(next_count)):
                    try: results.append(next(import_lbl))
                    except: next_limit = 'limit'
                output_text = [item for result in results for item in result]

                if list_act == "number":
                    output_text = [f'{i+1}. {item}' for i, item in enumerate(output_text)]
                    output_text = '\n'.join(output_text)
                else:
                    output_text = [f'{list_act}{item}' for item in output_text]
                    output_text = '\n'.join(output_text)

                count = output_text.count('\n') + 1
            except: flash('Something went Wrong...')
    
    if verbose: print('\033[33m[!!]\033[0m import_results:',output_text)
    return render_template('lp.html',   output_text=output_text,            input_text=input_text,
            start_target=start_target,  start_post_space=start_post_space,  start_post_enter=start_post_enter,
            end_target=end_target,      end_post_space=end_post_space,      end_post_enter=end_post_enter,
            cal_start=cal_start,        cal_end=cal_end,                    lbl_checkbox=lbl_checkbox,
            next_limit=next_limit,      count=count)

if __name__ == '__main__':
    app.run(debug=True)