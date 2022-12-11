import sqlite3, os.path, base64, json
from time import time,strftime, localtime, sleep

path_cwd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

DFLT_path = os.path.join(path_cwd,'static','data','test.db')
DFLT_table = 'home'
DFLT_data = {'username':'Reza','score':1,'total':15,'results':["string 1","string 2"]}
DFLT_cat = ['username','score']
DFLT_search = ['Reza',1]
DFLT_limit = 10
DFLT_update = {'username':'danish', 'total':10}
DFLT_rows = [1,2]
verbose = True

def convertToBinaryThenBase64(filename):
    # Convert digital data to binary format then base64 formate
    with open(filename, 'rb') as fout:
        blobData = fout.read()
        base64_data = base64.b64encode(blobData)
    return base64_data

def convertFromBase64ToBinary(base64Data):
    binaryData = base64Data.decode('utf-8')
    return binaryData

def writeTofile(base64Data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as fin:
        base64DataEncoded = base64Data.encode('utf-8')
        binary = base64.decodebytes(base64DataEncoded)
        fin.write(binary)
    print("Stored blob data into: ", filename, "\n")

# Where cat, search = [], []
def db_get(db_name=DFLT_path, table=DFLT_table, cat=DFLT_cat, search=DFLT_search):
    table = 'db' + str(table)
    
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    with conn:
        if '*' in search and len(search)==1 and '*' in cat and len(cat)==1:
            cursor.execute(f'SELECT * FROM {table}')
        elif '*' in search and len(search)==1 and len(cat)==1:
            one_cat = ''.join(cat)
            cursor.execute(f'SELECT * FROM {table} WHERE {one_cat} IS NOT NULL')
        elif '?' in search and len(search)==1 and '?' in cat and len(cat)==1:
            cursor.execute(f'SELECT * FROM {table}')
            items = cursor.fetchone().keys()
            return items
        else:
            categories =' AND '.join([f'{item} = ?' for item in cat])
            cursor.execute(f'SELECT * FROM {table} WHERE {categories}',search)
        
        items = [list(row) for row in cursor.fetchall()]
        return items

def db_give(db_name=DFLT_path, table=DFLT_table, data=DFLT_data):

    def convertToBinaryThenBase64(filename):
    # Convert digital data to binary format then base64 formate
        with open(filename, 'rb') as fout:
            blobData = fout.read()
            base64_data = base64.b64encode(blobData)
        return base64_data

    # Adding dates to data for tracking purposes
    data['date'] = strftime("%D %T", localtime()) 
    data['date_sec'] = time()

    data_tuple = []
    for cat in data:
        if isinstance(data[cat], str) and (data[cat][1:3] == f':{os.sep}'):
            data_tuple.append((f'{cat} BLOB NOT NULL', cat, convertToBinaryThenBase64(data[cat]),'?'))
        elif isinstance(data[cat], str):
            data_tuple.append((f'{cat} TEXT NOT NULL', cat, data[cat],'?'))
        elif isinstance(data[cat], (int,bool)):
            data_tuple.append((f'{cat} INTEGER NOT NULL', cat, data[cat],'?'))
        elif isinstance(data[cat], float):
            data_tuple.append((f'{cat} REAL NOT NULL', cat, data[cat],'?'))
        elif isinstance(data[cat], (list,dict,set)):
            data_tuple.append((f'{cat} TEXT NOT NULL', cat, json.dumps(data[cat]),'?'))
        else: 
            data_tuple.append((f'{cat} BLOB NOT NULL', cat, data[cat],'?'))
    
    # Extracting from data_tuple
    data_info, data_cat, data_val, q_markList = zip(*data_tuple)
           
    # Create the table statement (create_table)
    table = 'db' + str(table)
    columns = ', '.join(data_info) + ', id INTEGER PRIMARY KEY'
    create_table = f'CREATE TABLE IF NOT EXISTS {table}({columns})'

    # Create the insert statement (string_execute)
    category = ','.join(data_cat)
    q_marks = ','.join(q_markList)
    string_execute = f'INSERT INTO {table}({category}) VALUES({q_marks})'

    # Execute all statement 
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    with conn:
        cursor.execute(create_table)
        cursor.execute(string_execute, data_val)

    return string_execute+f', {str(data_cat)}'

def db_update(db_name=DFLT_path, table=DFLT_table, data=DFLT_update, cat=DFLT_cat, search=DFLT_search):
    
    table = 'db' + str(table)
    columns = ', '.join([f'{item} = ?' for item in data])
    
    data_val = []
    for item in data:
        if isinstance(data[item], str) and (data[item][1:3] == f':{os.sep}'):
            data_val.append(convertToBinaryThenBase64(data[item]))
        elif isinstance(data[item], (list,dict,set)):
            data_val.append(json.dumps(data[item]))
        else: data_val.append(data[item])

    if cat == ['*'] and search ==['*']:
        conditions = ''
    elif len(cat) == 1 and len(search) > 1:
        data_val.extend(search)
        q_marks = ','.join(['?' for _ in range(len(search))])
        conditions = 'WHERE ' + f'{cat[0]} IN ({q_marks})'
    elif len(cat) >= 1 and len(cat) == len(search):
        data_val.extend(search)
        conditions = 'WHERE ' + ' OR '.join([f'{ct} = ?' for ct in cat])
    else:
        if verbose:
            conditions, data_val, q_marks ='','',''
            print('\033[31m[!!] conditions: \033[0m', conditions)
            print('\033[31m[!!] data_val: \033[0m', data_val)
            print('\033[31m[!!] q_marks: \033[0m', q_marks)
            print('\033[31m[!!] db_update: \033[0m wrong parameters.')

    string_execute = f'UPDATE {table} SET {columns} {conditions}'

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    with conn:
        cursor.execute(string_execute, data_val)
    
    return string_execute

def db_deleteTable(db_name=DFLT_path, table=DFLT_table):

    table = 'db' + str(table)
    string_execute = f'DROP TABLE IF EXISTS {table}'

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    with conn:
        cursor.execute(string_execute)
    return string_execute

def db_deleteRow(db_name=DFLT_path, table=DFLT_table, cat=DFLT_cat, search=DFLT_search):

    # Create the delete statement(string_execute)
    table = 'db' + str(table)
    match_search = ' OR '.join([ temp_cat+' = '+str(temp_search) for temp_cat, temp_search in zip(cat,search)])
    string_execute = f'DELETE FROM {table} WHERE {match_search} ;'

    # Execute all statements
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    with conn:
        cursor.execute(string_execute)

    return string_execute

def db_tableNames(db_name=DFLT_path):

    string_execute = "SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%'"

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    with conn:
        cursor.execute(string_execute)
        items = [row[0][2:] for row in cursor.fetchall()]
    return items

def delete_table(db_name=DFLT_path):

    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    
    table_info = []
    for stuff in cursor.fetchall():
        for table_name in stuff:
            table_info.append((table_name[2:],table_name[-1:]))

    for nm, hour in table_info:
        cursor.execute(f'SELECT * FROM db{nm}')
        date_sec = int(cursor.fetchone()['date_sec'])
        time_diff = round(time() - date_sec)/3600
        if time_diff > int(hour):
            cursor.execute(f"DROP TABLE IF EXISTS db{nm}")
            print(f"Table db{nm} has been deleted")
        else:
            left_time = abs(int(hour) - time_diff)
            print(f'Failed to drop db{nm}.  Time left: {left_time}')

    print(table_info)

def limit_cat_size(db_name=DFLT_path, table=DFLT_table, cat=DFLT_cat, limit=10):
    get_items = db_get(db_name, table, cat, ['*'])
    if len(get_items) > limit:
        oldest = str(min([id for id, _, _, _ in get_items]))
        print(oldest)
        delete_row(db_name, table, ['id'], [oldest])
    print('size:',len(get_items))

def add_count_rows(db_name=DFLT_path, table=DFLT_table, cat=DFLT_cat):
    table = 'db' + str(table)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    string_execute = 'SELECT '+' + '.join([f"COUNT('{ct}')" for ct in cat])+f' FROM {table}'
    cursor.execute(string_execute)
    # print(string_execute)
    count = list(cursor.fetchone())[0]
    return count



if __name__ == "__main__":
    # path_ideas = os.path.join(path_cwd,'static','ideas','ideas.db')
    # data = {'comment':'some text','mylist':['test',3,4]}
    # db_give(db_name=DFLT_path, table='another_test', data=data)
    # sav = db_get(db_name=DFLT_path, table='another_test', cat=['*'], search=['*'])
    
   

    # limit_cat_size(db_name=path_ideas, table='comments', cat=['comment'], limit=5)
    # test = db_tableNames(db_name=DFLT_path)
    path_class = os.path.join(path_cwd,'static','data','class.db')
    # dataReply = {'passOut': [], 'ready': [], 'waiting': ['Pete', 'Sam']}
    mylist = ['pete','john']
    test = {'waiting': mylist}
    stat = db_update(db_name=path_class, table='9428', data=test, cat=['id'], search=[1])
 