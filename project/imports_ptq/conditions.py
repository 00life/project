
def cond(period_start=1,period_end=1,questions=1):

    #msg_false1 = set()
    msg_false2 = set()

    # if not isinstance(period_start,int):
    #     msg_false1.add((False, "Period Start must be an integer"))
    # if not isinstance(period_end,int):
    #     msg_false1.add((False, "Period End must be an integer"))
    # if not isinstance(questions,int):
    #     msg_false1.add((False, "Number of Questions must be an integer"))
    
    # if False in {boolean for boolean,_ in msg_false1}:
    #     return msg_false1

    if period_start < 1:
        msg_false2.add((False, "Period Start cannot be less than 1"))
    if period_end < 1:
        msg_false2.add((False, "Period End cannot be less than 1"))
    if questions < 0:
        msg_false2.add((False, "Number of Questions cannot be less than 0"))
    if abs(period_end - period_start + 1) < questions:
        msg_false2.add((False, "There must be More Periodic Elements than questions"))
    if period_end < period_start:
        msg_false2.add((False, "Period Start cannot be less than Period End"))

    if False in {boolean for boolean,_ in msg_false2}:
        return msg_false2
    
    return {(True,'')}

if __name__ == '__main__':
    print(cond())

    # dict_1 = {
    #     "Period Start must be an integer": period_start,
    #     "Period End must be an integer": period_end,
    #     "Number of Questions must be an integer": questions}

    # for msg in dict_1:
    #     num_set = {ord(i) for i in str(dict_1[msg])}
    #     boolean = all({True if num in range(48,58) else False for num in num_set})
    #     msg_false1.add((False, msg)) if boolean is False else msg_false1

    # if False in {boolean for boolean,_ in msg_false1}:
    #     return msg_false1
