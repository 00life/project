import re, pickle

verbose = True
DV_st = 'CSS' ; DV_sps = 1; DV_spe = 0; DV_cal_s = 0
DV_et = 'CSS' ; DV_eps = 2; DV_epe = 0 ; DV_cal_e = 0
DV_txt = """ CSS HOME23 HOME CSS Intro HOME CSS Syntax HOME342
HOME CSS Intro HOME CSS Syntax HOME342
OME23 HOME CSS Intro HOME CS"""

def final_indexes1(target_indexes,space_indexes,input_space):

    final_indexes2 = []
    for index in target_indexes:
        count = 0
        temp_indexes = []
        for space in space_indexes:
            if input_space > 0:
                if space > index-1:
                    temp_indexes.append(space)
                    count+=1
                    if count >= abs(input_space):
                        break
            else:
                if space < index:
                    temp_indexes.append(space)
                    count+=1
                    if count >= abs(input_space):
                        break
        
        final_indexes2.append(temp_indexes[-1])

    return final_indexes2

def target_indices(target,text,start_end):

    if target.find('\w'):
        target = target.replace('\w','[a-zA-Z]')
    if target.find('\c'):
        target = target.replace('\c','[a-z]')
    if target.find('\C'):
        target = target.replace('\c','[A-Z]')
    if target == '\\' and start_end == 'start':
        return [],[0]
    if target == '\\\\' and start_end == 'end':
        return [len(text)], []

    start, end = [], []
    for match in re.finditer(target,text):
        start.append(match.start())
        end.append(match.end())
    
    return start, end

def row_data_list_func(text,spaces,sp_dir):
    enters = []
    for match in re.finditer('\n',text):
        enters.append(match.start())
    enters.append(len(text))

    first_last = []
    for i in range(1,len(enters)):
        first_last.append([enters[i-1]+1,enters[i]])
    first_last.insert(0,[0,enters[0]])

    text_info = []
    for num,(first,last) in enumerate(first_last):
        sp_indexes = []
        for sp_inx in spaces:
            if sp_inx > first and sp_inx < last:
                sp_indexes.append(sp_inx)
        if sp_dir == 'forward':
            sp_indexes.insert(0,first)
            sp_indexes.append(last)
        elif sp_dir == 'backward':
            sp_indexes.insert(0,last)
            sp_indexes.append(first)

        text_info.append(({'row':num,'len':len(sp_indexes),'inx':sp_indexes}))

    return text_info

def final_indexes2(row_data_list,tgt_indexes,enter_pos,space_pos):

    abs_space_pos = abs(space_pos)

    index_location = set()
    for tgt_index in tgt_indexes:
        for row_data in row_data_list:
            if space_pos >= 0:
                if tgt_index > row_data['inx'][0] and tgt_index < row_data['inx'][-1]:
                    index_location.add((row_data['row'] + enter_pos, abs_space_pos))
            elif space_pos < 0:
                if tgt_index < row_data['inx'][0] and tgt_index > row_data['inx'][-1]:
                    index_location.add((row_data['row'] + enter_pos, abs_space_pos))

    result_index = []
    for row,sp in index_location:
        for row_data in row_data_list:
            if row == row_data['row']:
                if abs_space_pos > row_data['len'] - 1:
                    result_index.append(row_data['inx'][-1])
                else:
                    result_index.append(row_data['inx'][abs_space_pos])

    return sorted(result_index)

def evaluate(start_tgt=DV_st,sps=DV_sps,spe=DV_spe,
    end_tgt=DV_et,eps=DV_eps,epe=DV_epe,text=DV_txt,
    cal_s=DV_cal_s,cal_e=DV_cal_e):

    fix_s, fix_e = 0,0

    # Getting the start & end indexes of the targets (st and et)
    tgt_start_s, tgt_end_s = target_indices(start_tgt,text,'start') 
    tgt_start_e, tgt_end_e = target_indices(end_tgt,text,'end')

    # Getting the indexes of all the spaces in the text
    spaces_for, spaces_bac = [], []
    for match in re.finditer(' ',text):
        spaces_for.append(match.start()) # accending order
        spaces_bac.insert(0,match.start()) # decending order

    # An enter value was inputed for the starting target
    if spe != 0 and sps >= 0:
        spe_map = row_data_list_func(text=DV_txt,spaces=spaces_for,sp_dir='forward')
        start_inx = final_indexes2(row_data_list=spe_map,tgt_indexes=tgt_start_s,enter_pos=spe,space_pos=sps)
        if sps == 0: fix_s = -1
    elif spe != 0 and sps < 0:
        spe_map = row_data_list_func(text=DV_txt,spaces=spaces_bac,sp_dir='backward')
        start_inx = final_indexes2(row_data_list=spe_map,tgt_indexes=tgt_start_s,enter_pos=spe,space_pos=sps)
    # No enter value was inputed for the starting target
    elif spe == 0 and sps > 0:
        start_inx = final_indexes1(tgt_end_s,spaces_for,sps)
    elif spe == 0 and sps < 0:
        start_inx = final_indexes1(tgt_start_s,spaces_bac,sps)
    elif spe == 0 and sps == 0:
        start_inx = tgt_end_s
        fix_s = - 1

    # An enter value was inputed for the ending target
    if epe != 0 and eps >= 0:
        epe_map = row_data_list_func(text=DV_txt,spaces=spaces_for,sp_dir='forward')
        end_inx = final_indexes2(row_data_list=spe_map,tgt_indexes=tgt_start_s,enter_pos=epe,space_pos=eps)
    elif epe != 0 and eps < 0:
        epe_map = row_data_list_func(text=DV_txt,spaces=spaces_bac,sp_dir='backward')
        end_inx = final_indexes2(row_data_list=spe_map,tgt_indexes=tgt_start_s,enter_pos=epe,space_pos=eps)
    # No enter value was inputed for the ending target
    elif epe == 0 and eps > 0:
        end_inx = final_indexes1(tgt_end_e,spaces_for,eps)
    elif epe == 0 and eps < 0:
        end_inx = final_indexes1(tgt_start_e,spaces_bac,eps)
    elif epe == 0 and eps == 0:
        end_inx = tgt_start_e

    slice_indexes = []
    for si in start_inx:
        for ei in end_inx:
            if ei >= si:
                slice_indexes.append((si,ei))
                break
    
    word_list = [text[ s_inx+1 + fix_s + cal_s : e_inx + fix_e + cal_e ] for s_inx,e_inx in slice_indexes]
    
    # if verbose:
        # print('\033[32m[!!]\033[0m list_parser results:', word_list)
        # print('\033[32m[!]\033[0m slice_indexes:',slice_indexes)
        # print('(\033[32m[+]\033[0m start_inx:',start_inx,')','(\033[31m[-]\033[0m end_inx:',end_inx,')')
        # print('\033[32m[+]\033[0m tgt_start_s:',tgt_start_s,'\033[31m[-]\033[0m tgt_end_s:',tgt_end_s)
        # print('\033[33mspace_for:\033[0m',spaces_for)
        # print('\033[34mspace_bac:\033[0m',spaces_bac)
    for word in word_list:
        yield  word

def line_by_line(split_text=DV_txt,
                start_tgt=DV_st,sps=DV_sps,spe=DV_spe,
                end_tgt=DV_et,eps=DV_eps,epe=DV_epe,
                cal_s=DV_cal_s,cal_e=DV_cal_e):

    lbl_text = split_text.split('\n')
    next_lbl_list = []
    for line in lbl_text:
        line_results = evaluate(start_tgt,sps,spe,end_tgt,eps,epe,line,cal_s,cal_e)
        next_lbl_list.append(line_results)

    for next_lbl in next_lbl_list:
        yield next_lbl

if __name__ == '__main__':
    a = list(evaluate())
    print(a)
    # line_by_line()
    pass