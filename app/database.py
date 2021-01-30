from flask import current_app, jsonify
from sqlalchemy import create_engine, select
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import email
from email import policy
from email.parser import BytesParser
import base64

import os
from shutil import copy2

import hashlib
import random
import string


from app import db

engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

def get_user_salt(username):
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    sql = "exec System.GetUserSalt @username=?"
    try:
        cursor.execute(sql, username)
        result = cursor.fetchone()
        return str(result[0])
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return 'Error'
    finally:
        cursor.close()

def set_user_salt():
        characters = string.hexdigits + string.punctuation
        characters = characters.replace("\'", "")
        characters = characters.replace('\"', "")
        salt = ''.join(random.choice(characters) for i in range(16))
        return salt

def hash_password(salt, password):
    password_to_check = salt[:8] + password + salt[8:]
    hash_object = hashlib.sha256(password_to_check.encode())
    hashed_password = hash_object.hexdigest().upper()
    return hashed_password

def get_user_info(username, hashed_password):
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    sql = "exec System.GetUserInfo @username=?, @passwordhash=?"
    try:
        cursor.execute(sql, [username, hashed_password])
        result = cursor.fetchone()
        return result
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return 'Error'
    finally:
        cursor.close()



def create_user(role, username, firstname, lastname, passwordhash, passwordsalt):
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    sql = "exec System.CreateUser @role=?, @username=?, @firstname=?, @lastname=?, @passwordhash=?, @passwordsalt=?;"

    try:
        result = cursor.execute(sql, [role, username, firstname, lastname, passwordhash, passwordsalt])
        cursor.commit()
        return 'OK'
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return 'Error'
    finally:
        cursor.close()

def change_password(user_id, hashed_password):
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    sql = "exec System.UpdateUserPasswordHash @userid=?, @passwordhash=?;"

    try:
        result = cursor.execute(sql, [user_id, hashed_password])
        cursor.commit()
        return 'OK'
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return 'Error'
    finally:
        cursor.close()



def get_cases():
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    sql = "exec dbo.GetCases"
    result_dict={}
    
    cases=[]
    try:
        result = cursor.execute(sql).fetchall()
        for row in result:
            result_dict={
                "caseID" : row[0],
                "code" : row[1],
                "stateID": row[2],
                "status" : row[3],
                "caseType" : row[4],
                "created": row[7].strftime("%d-%m-%Y %H:%M:%S"),
                "modified" : row[8].strftime("%d-%m-%Y %H:%M:%S"),
                "display": {},
                "buttons": {},
                "info" : {}

            }
            cases.append(result_dict)
        return cases
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return 'Error'
    finally:
        cursor.close()

def get_case_items(case_id):
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    sql = "exec dbo.GetCaseItems @caseid=?"
    result_dict={}
    case_items=[]
    try:
        result = cursor.execute(sql, [case_id]).fetchall()
        for row in result:
            result_dict={
                "itemID" : row[0],
                "caseID" : row[1],
                "typeID": row[2],
                "emailFrom" : row[3],
                "emailTo" : row[4],
                "emailCc" : row[5],
                "dateTime" : row[6].strftime("%d-%m-%Y %H:%M:%S"),
                "buttons": {},
                "info" : {}
            }
            case_items.append(result_dict)
        return case_items
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return 'Error'
    finally:
        cursor.close()

def close_case(case_id, state_id, user_id):
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    
    if state_id != '140':
        state_id = 130
    else:
        print("something else") # <-- treba message pre usera
    
    sql = "exec dbo.ChangeCaseState @caseid=?, @stateid=?, @userid=?"
    try:
        result = cursor.execute(sql, [case_id, state_id, user_id])
        cursor.commit()
        return 'OK'
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return 'Error'
    finally:
        cursor.close()

def remove_case(case_id, state_id, user_id):
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    state_id = 140

    sql = "exec dbo.ChangeCaseState @caseid=?, @stateid=?, @userid=?"
    try:
        result = cursor.execute(sql, [case_id, state_id, user_id])
        cursor.commit()
        return 'OK'
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return 'Error'
    finally:
        cursor.close()

def change_state_of_case(case_id, state_id, user_id):
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    sql = "exec dbo.ChangeCaseState @caseid=?, @stateid=?, @userid=?"
    try:
        result = cursor.execute(sql, [case_id, state_id, user_id])
        cursor.commit()
        return 'OK'
    except Exception as e:
        print("stored procedure {} returning error: {}".format(sql, e))
        return 'Error'
    finally:
        cursor.close() 


def get_cases_by_state(state_id):
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    sql = "exec dbo.GetCasesByStateId @stateid=?"
    result_dict={}
    removed_cases=[]
    try:
        result = cursor.execute(sql,[state_id]).fetchall()
        for row in result:
            result_dict={
                "caseID" : row[0],
                "code" : row[1],
                "stateID": row[2],
                "status" : row[3],
                "caseType" : row[4],
                "created": row[7].strftime("%d-%m-%Y %H:%M:%S"),
                "modified" : row[8].strftime("%d-%m-%Y %H:%M:%S"),
                "display":{},
                "buttons" : {}

            }
            removed_cases.append(result_dict)
        return removed_cases
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return 'Error'
    finally:
        cursor.close()

def create_case_item(caseid, typeid, emailfrom, emailto, emailcc):
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    sql = 'exec dbo.CreateCaseItem @caseid=?, @typeid=?, @emailfrom=?, @emailto=?, @emailcc=?'
    try:
        result = cursor.execute(sql, [caseid, typeid, emailfrom, emailto, emailcc]).fetchone()
        cursor.commit()
        return result
    except Exception as e:
        print("stored procedure {} returning error: {}".format(sql, e))
        return 'Error'
    finally:
        cursor.close()

def verify_case_item(case_id, state_id, user_id):
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()

    if state_id in ['20', '60', '100']:
        state_id = (int(state_id) + 10)
    else:
        print("state could not be confirmed") # <-- treba message pre usera

    sql_state = "exec dbo.ChangeCaseState @caseid=?, @stateid=?, @userid=?"
    sql_log = "exec dbo.CreateItemLog @itemid=?, @userid=?, @level=?, @text=?"
    try:
        result = cursor.execute(sql_state, [case_id, state_id, user_id])
        cursor.commit()
        return state_id
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return 'Error'
    finally:
        cursor.close()

def remove_case_item(case_id, state_id, user_id):
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()

    if state_id in ['20', '30', '40']:
        state_id = 50
    elif state_id in ['60', '70']:
        state_id = 80
    elif state_id in ['100', '110']:
        state_id = 120
    else:
        print("item could not be removed") # <-- treba message pre usera

    sql = "exec dbo.ChangeCaseState @caseid=?, @stateid=?, @userid=?"
    try:
        result = cursor.execute(sql, [case_id, state_id, user_id])
        cursor.commit()
        return state_id
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return 'Error'
    finally:
        cursor.close()

def get_case_logs(case_id):
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    sql = "exec dbo.GetCaseLogs @caseid=?"
    result_dict={}
    case_logs=[]
    try:
        result = cursor.execute(sql, [case_id]).fetchall()
        for row in result:
            result_dict={
                "datetime" : row[0].strftime("%d-%m-%Y %H:%M:%S"),
                "username" : row[1],
                "level": row[2],
                "text" : row[3]
            }
            case_logs.append(result_dict)
        return case_logs
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return 'Error'
    finally:
        cursor.close()


def get_item_logs(item_id):
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    sql = "exec dbo.GetItemLogs @itemid=?"
    result_dict={}
    case_items_logs=[]
    try:
        result = cursor.execute(sql, [item_id]).fetchall()
        for row in result:
            result_dict={
                "datetime" : row[0].strftime("%d-%m-%Y %H:%M:%S"),
                "username" : row[1],
                "level": row[2],
                "text" : row[3]
            }
            case_items_logs.append(result_dict)
        return case_items_logs
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return 'Error'
    finally:
        cursor.close()

def create_item_logs(item_id, user_id, text):
    level = "Info"
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    sql = "exec dbo.CreateItemLog @itemid=?, @userid=?, @level=?, @text=?"
    try:
        result = cursor.execute(sql, [item_id, user_id, level, text])
        cursor.commit()
        return 'OK'
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return 'Error'
    finally:
        cursor.close()

def get_item_files(item_id):
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    sql = "exec dbo.GetItemFiles @itemid=?"
    result_dict={}
    item_files=[]
    try:
        result = cursor.execute(sql, [item_id]).fetchall()
        for row in result:
            result_dict={
                "fileid" : row[0],
                "path" : row[1],
                "name": row[2],
                "extension" : row[3],
                "size" : row[4],
                "hash" : row[5],
                "datetime" : row[6].strftime("%d-%m-%Y %H:%M:%S")
            }
            item_files.append(result_dict)
        return item_files
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return 'Error'
    finally:
        cursor.close()

def display_eml(eml_filepath): ## -> treba vyladit!!!
    with open(eml_filepath, 'rb') as eml_file:

        msg = BytesParser(policy=policy.default).parse(eml_file)
        text = msg.get_body(preferencelist=('plain')).get_content()
        # sk = get_info_from_mail_field(msg['from'])
        # eml_output = eml_file.read()
        eml_output = msg
        # eml_output = msg #get_all('Content-Dispositio
        found = []
        for part in msg.walk():
            if 'content-disposition' not in part:
                continue
            cdisp = part['content-disposition'].split(';')
            cdisp = [x.strip() for x in cdisp]
            if cdisp[0].lower() != 'attachment':
                continue
            parsed = {}
            for kv in cdisp[1:]:
                key, val = kv.split('=')
                if val.startswith('"'):
                    val = val.strip('"')
                elif val.startswith("'"):
                    val = val.strip("'")
                parsed[key] = val
            found.append((parsed, part))
        eml_output = {
                     "Odesílatel": msg.get('From'),
                     "Příjemce": msg.get('To'),
                     "Datum": msg.get('Date'),
                     "Předmět": msg.get('Subject'),
                     "Text zprávy": msg.get_body(preferencelist=('plain')).get_content(),
                     "Přílohy": found #[0]
                     }
        #print('eml_output',eml_output, msg.get('Cc'))
        if msg.get_content_maintype() == 'multipart':  # <--zjisti zda potrebujes - jinak smaz
            # loop on the parts of the mail
            for part in msg.walk():
            # find the attachment part - so skip all the other parts
                if part.get_content_maintype() == 'multipart': continue
                if part.get_content_maintype() == 'text':
                    content = part.get_body(preferencelist=('plain'))
                    if content:
                        output = part.get_body(preferencelist=('plain')).get_content()
                    else:
                        output = None
                    continue
                if part.get('Content-Disposition') == 'inline': continue
                if part.get('Content-Disposition') is None: continue
                # save the attachment in the program directory
                result_dict = {
                     "Odesílatel": msg.get('From'),
                     "Příjemce": msg.get('To'),
                     "Datum": msg.get('Date'),
                     "Předmět": msg.get('Subject'),
                     "Text zprávy": output, #msg.get_body(preferencelist=('plain')).get_content(),
                     "Přílohy": part.get_all('Content-Disposition')
                     }
                #eml_output = result_dict
                #print('result_dict',result_dict)
    return eml_output

def display_items(item_files):
    pdf_output = None
    eml_output = None
    xlsx_output = None
    for i in item_files:
        if i.endswith('pdf'):
            print('pdf')
            try:
                with open(i, "rb") as pdf_file:
                    pdf_output = (base64.b64encode(
                        pdf_file.read())).decode('ascii')
            except Exception as e:
                print('error', str(e))
                continue
        elif i.endswith('eml'):
            eng_code,filename = i.split('\\')[-2:]
            filename = filename.split(".")[0]
            print('eml')
            try:
                eml_output = display_eml(i)
                eml_output['Filename'] = filename
                eml_output['Eng_code'] = eng_code
            except Exception as e:
                print('error', str(e))
                continue
        elif i.endswith('.xlsx'):
            xlsx_output = '.xlsx'
        else:
            print(i)
    return [eml_output , pdf_output, xlsx_output]



def get_state_by_caseid(case_id):
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    sql = "exec dbo.GetCaseByCaseId @caseid=?"
    try:
        result = cursor.execute(sql, [case_id]).fetchone()
        print (result)
        return result
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return 'Error'
    finally:
        cursor.close()

def get_cases_by_code(code): 
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    sql = "exec dbo.GetCasesByCode @code=?"
    result_dict={}
    item_files=[]
    try:
        result = cursor.execute(sql,[code]).fetchall()
        for row in result:
            result_dict={
                "caseID" : row[0],
                "code" : row[1],
                "stateID": row[2],
                "status" : row[3],
                "caseType" : row[4]
                "created": row[7].strftime("%d-%m-%Y %H:%M:%S"),
                "modified" : row[8].strftime("%d-%m-%Y %H:%M:%S"),
                "display":{},
                "buttons" : {}
            }
            item_files.append(result_dict)
        return item_files
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return None
    finally:
        cursor.close()

def get_case_by_caseId(caseid):
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    sql = "exec dbo.GetCaseByCaseId @caseid=?"
    result_dict={}
    try:
        result = cursor.execute(sql,[caseid]).fetchone()
        result_dict={
            "caseID" : result[0],
            "code" : result[1],
            "stateID": result[2],
            "status" : result[3],
            "caseType" : result[4]
        }
        return result_dict
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return None
    finally:
        cursor.close()


def get_sender_contact_type(item_id):
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    sql = "exec dbo.GetContactTypeByItemId @itemid=?"
    try:
        result = cursor.execute(sql, [item_id]).fetchone()
        return result
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return 'Error'
    finally:
        cursor.close()

def get_file_contact_type(item_id):
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    sql = "exec dbo.GetItemByItemId @itemid=?"
    try:
        result = cursor.execute(sql, [item_id]).fetchone()
        return result
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return 'Error'
    finally:
        cursor.close()

def get_settings(key):
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    sql = "exec System.ReadCurrentSetting @PairKey=?"
    try:
        result = cursor.execute(sql, [key]).fetchone()
        return result
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return 'Error'
    finally:
        cursor.close()


def get_aggregated_cases(category):
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    sql = "exec dbo.GetAgregBy" + category
    result_dict={}
    item_files=[]
    try:
        result = cursor.execute(sql).fetchall()
        if category == 'Status':
            for row in result:
                result_dict={
                    "category" : row[0],
                    "count" : row[2],
                    "button" : row[1]
                }
                item_files.append(result_dict)
            return item_files
        else:
            for row in result:
                result_dict={
                    "category" : row[0],
                    "count" : row[1],
                    "button" : ""
                    }
                item_files.append(result_dict)
            return item_files
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return 'Error'
    finally:
        cursor.close()

def get_aggregated_subcategory_cases(category,subcategory):
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    if category == 'EngCode':
        sql = "exec dbo.GetCasesByCode @code=?"
    elif category == 'Status':
        sql = "exec dbo.GetCasesByStateId @stateid=?"
    elif category == 'Type':
        sql = "exec dbo.GetCasesByType @type=?"
    elif category == 'Created':
        sql = "exec dbo.GetCasesByCreated @year=?, @month=?"
        year = subcategory.split(':')[0]
        month = subcategory.split(':')[1]
    elif category == 'Modified':
        sql = "exec dbo.GetCasesByModified @year=?, @month=?"
        year = subcategory.split(':')[0]
        month = subcategory.split(':')[1]
    

    result_dict={}
    item_files=[]
    try:
        if category in ['Created', 'Modified']:
            result = cursor.execute(sql,[year, month]).fetchall()
        else:
            result = cursor.execute(sql,[subcategory]).fetchall()
        for row in result:
            result_dict={
                "caseID" : row[0],
                "code" : row[1],
                "stateID": row[2],
                "status" : row[3],
                "caseType" : row[4],
                "created": row[7].strftime("%d-%m-%Y %H:%M:%S"),
                "modified" : row[8].strftime("%d-%m-%Y %H:%M:%S"),
                'button' : {},
                'buttons': [row[0], row[2]],
                'i_button:' : {}
            }
            item_files.append(result_dict)

        return item_files
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return 'Error'
    finally:
        cursor.close()

def get_unprocessed_emails():
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    sql = "exec dbo.GetEmails" 
    result_dict={}
    item_files=[]
    try:
        result = cursor.execute(sql).fetchall()
        for row in result:
            result_dict={
                "emailID" : row[0],
                "fileID" : row[1],
                "stateID": row[2],
                "sender" : row[3],
                "subject" : row[4],
                "recieved": row[5].strftime("%d-%m-%Y %H:%M:%S"),
                "created": row[6].strftime("%d-%m-%Y %H:%M:%S"),
                "modified" : row[7].strftime("%d-%m-%Y %H:%M:%S"),
                "messageID": row[8],
                "conversationID" : row[9],
                "itemID": row[10],
                "path": row[11],
                "name": row[12],
                "extension": row[13],
                "size": row[14],
                #"hash": row[15],
                'display_button' : {}
            }
            item_files.append(result_dict)
        return item_files
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return 'Error'
    finally:
        cursor.close()

def get_email_by_emailId(email_id):
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    sql = "exec dbo.GetEmailByEmailId @emailid=?"
    result_dict={}
    try:
        result = cursor.execute(sql,[email_id]).fetchone()
        result_dict={
            "emailID" : result[0],
            "fileID" : result[1],
            "stateID": result[2],
            "sender" : result[3],
            "subject" : result[4],
            "recieved": result[5],#.strftime("%d-%m-%Y %H:%M:%S"),
            "created": result[6],#.strftime("%d-%m-%Y %H:%M:%S"),
            "modified" : result[7], #.strftime("%d-%m-%Y %H:%M:%S")
            "messageID": result[8],
            "conversationID" : result[9],
            "path" : result[10],
            "name" : result[11],
            "extension" : result[12]

        }
        return result_dict
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return 'Error'
    finally:
        cursor.close()


def change_email_state(email_id, state_id):
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    sql = "exec dbo.ChangeEmailState @emailid=?, @stateid=?"
    try:
        result = cursor.execute(sql,[email_id, state_id])
        cursor.commit()
        return 'OK'
    except Exception as e:
        print("stored procedure returning error: {}".format(e))
        return 'Error'
    finally:
        cursor.close()

def uniquify_filename(filePath):
    filename, extension = os.path.splitext(filePath)
    counter = 1
    while os.path.exists(filePath):
        filePath = filename + "_(" + str(counter) + ")" + extension
        #filePath = filePath.replace(" ", "_")
        counter += 1
    return filePath

def replace_email_file(email_id, item_id, case_id):

    UPLOAD_FOLDER = get_settings('PathToFiles')[1]

    email_info = get_email_by_emailId(email_id)
    att_path = email_info['path']
    att_name = email_info['name']
    att_ext = email_info['extension']
    att_filename = att_name + '.' + att_ext
    current_filepath = os.path.join(UPLOAD_FOLDER,att_path,att_filename)

    case_info = get_case_by_caseId(case_id)
    eng_code = case_info['code']
    new_path = os.path.join(eng_code, str(case_id).zfill(8))
    new_dir = os.path.join(UPLOAD_FOLDER, eng_code, str(case_id).zfill(8))
    new_filename = '['+ str(item_id).zfill(8) + '].' + att_ext
    new_filepath = os.path.join(new_dir, new_filename)
    if not os.path.exists(new_dir):
         os.makedirs(new_dir)

    copy2(current_filepath, new_filepath)
    return  new_filepath, new_filename, new_path

def get_hashed_file(filePath):
    block_size = 65536
    file_hash = hashlib.sha256()
    with open(filePath, 'rb') as f:
        fb = f.read(block_size)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(block_size)
    hash_file = file_hash.hexdigest()

    return hash_file

def create_file(itemid, filepath, filename, extension, size, hash_file):
    
    conn = engine.connect()
    cursor = engine.raw_connection().cursor()
    sql = "exec Storage.CreateFile @itemid=?, @path=?, @name=?, @extension=?, @size=?, @hash=?"
    try:
        result = cursor.execute(sql, [itemid, filepath, filename, extension, size, hash_file]).fetchone()
        cursor.commit()
        return result
    except Exception as e:
        print("stored procedure {} returning error: {}".format(sql, e))
        return 'Error'
    finally:
        cursor.close()

