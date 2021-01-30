
from flask import render_template, url_for, redirect, request, current_app, flash, jsonify, send_file, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
from sqlalchemy.engine import url
import base64
import pandas


import glob
import os


from . import user
from app import db
from app.models import User
from app.database import *
from app.user.forms import ClassificationForm


@user.route('/user/<username>')
@login_required
def userProfile(username):
    user = User.query.filter_by(UserName=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user/userProfile.html', user=user, posts=posts)

@user.route('/user/display/case_id_<case_id>/logs')
@login_required
def displayCaseLogs(case_id):
    print('BRANCH: /user/display/case_id_<case_id>/logs ')
    headers2 = ['Datum', 'Uživatel', 'Úroveň', 'Popis']
    case_logs = get_case_logs(case_id)
    title = 'Historie změn:'
    return render_template('user/displayLogs.html', headers2=headers2, logs=case_logs, title=title)


@user.route('/user/browse/case_id_<case_id>')
@login_required
def browseCaseItems(case_id):
    print('BRANCH: /user/browse/case_id_<case_id>')
    state = get_state_by_caseid(case_id)[3]

    headers = ['ID Položky', 'ID Případu', 'Datum', '', '']
    state_id = request.args.get('state_id')
    items = get_case_items(case_id)
    
    if items == []:
        return render_template('errors/noFile.html')
    else:
        return render_template('user/browseCaseItems.html', headers=headers, objects=items, case_id=case_id, status=state)

@user.route('/user/remove_case_item', methods=['GET', 'PUT']) 
@login_required
def removeCaseItem():
    skuska = request.get_data()
    case_id = request.form.get("case_id")
    state_id = request.form.get('state_id')
    user_id = current_user.UserId
    update = remove_case_item(case_id, state_id, user_id)

    return jsonify({"newStateID": update})


@user.route('/user/display/case_id_<case_id>/item_id_<item_id>/logs')
@login_required
def displayItemLogs(case_id, item_id):
    print('BRANCH: /user/display/case_id_<case_id>/item_id_<item_id>/logs')
    headers2 = ['Datum', 'Uživatel', 'Úroveň', 'Popis']
    item_logs = get_item_logs(item_id)
    title = 'Historie změn položky:'
    return render_template('user/displayLogs.html', headers2=headers2, logs=item_logs, title=title)


@user.route('/user/create_case_item_log', methods=['GET', 'PUT']) 
def createItemLog():
    item_id = request.form.get("item_id")
    user_id = current_user.UserId
    text = request.form.get("text")
    item_log = create_item_logs(item_id, user_id, text)

    return 'OK'


@user.route('/user/display/case_id_<case_id>/item_id_<item_id>')
@login_required
def displayItem(case_id, item_id):

    print('BRANCH: /user/display/case_id_<case_id>/item_id_<item_id>')

    state_id = get_state_by_caseid(case_id)[2]
    type_of_contact = get_file_contact_type(item_id)[2]
    contact_type = None
    try:
        contact_type = get_sender_contact_type(item_id)[7]
    except:
        pass

    uploadFolder =  get_settings('PathToFiles')[1]

    item_files = []
    try:
        files = get_item_files(item_id)
        # create list of files with same item ID
        for f in files:
            extension = f['extension']
            path = f['path']
            name = f['name']
            filename = name + '.' + extension
            one_file = os.path.join(uploadFolder, path, filename)
            item_files.append(one_file)
    except IndexError:
        return render_template('errors/404.html')

    eml_output, pdf_output, xlsx_output = display_items(item_files)

    if pdf_output is None and eml_output is None:
        return render_template('errors/noData.html')
    else:
        return render_template ('user/displayItem.html', pdf_output = pdf_output, eml_output = eml_output, xlsx_output =xlsx_output, state_id = state_id, type_of_contact=type_of_contact, contact_type=contact_type)

@user.route('/user/browse/aggregatedBy<category>')
@login_required
def aggregated(category):
    print('BRANCH: /user/browse/aggregatedBy<category>')
    headers = ['Kategorie', 'Počet', '']
    items =  get_aggregated_cases(category)
    if items == []:
        return render_template('errors/noData.html')
    elif items == 'Error':
        return render_template('errors/500.html') # dopln do ostatnych views!!!!!
    else:
        return render_template('user/browseCasesAggregated.html', headers = headers, objects = items, category = category)


@user.route('/user/browse/aggregatedBy<category>/<subcategory>')
@login_required
def aggregated_subcategory(category, subcategory):
    print('BRANCH: /user/browse/aggregatedBy<category>/<subcategory>')
    headers = ['ID Případu ', 'Kód', 'ID Stavu', 'Stav případu',  'Typ případu', "Případ vytvořen", "Naposledy upraveno",'', '','']
    items2 =  get_aggregated_subcategory_cases(category,subcategory)
    if items2 == []:
        return render_template('errors/noData.html')
    elif items2 == 'Error':
        return render_template('errors/500.html')
    else:
        return render_template('user/browseCasesByCategory.html', headers = headers, objects = items2, category = category, subcategory = subcategory)


@user.route('/user/browse/unclassified') 
@login_required
def unclassified():
    print('BRANCH: /user/browse/unclassified')
    headers = ['ID Emailu ', 'ID souboru', 'ID Stavu', 'Odesílatel',  'Předmět','Email přijat',"Vytvořeno", "Upraveno","","",'ID položky', 'Cesta', "Název", "Koncovka","Velikost",  '']
    items = get_unprocessed_emails()
    if items == []:
        return render_template('errors/noData.html')
    elif items == 'Error':
        return render_template('errors/500.html')
    else:
        return render_template('user/unclassified.html', headers = headers, objects = items)

@user.route('/user/display/email_id_<email_id>')
@login_required
def displayEmail(email_id):
    print('BRANCH: /user/display/email_id_<email_id>')
    email = get_email_by_emailId(email_id)
    uploadFolder =  get_settings('PathToFiles')[1]
    if email == {}:
        return render_template('errors/noData.html')
    elif email == 'Error':
        return render_template('errors/500.html') # dopln do ostatnych views!!!!!
    else:
        name = email['name'] + '.' + email['extension']
        file = os.path.join(email['path'], name)
        filepath = os.path.join(uploadFolder,file)
        eml_output = display_eml(filepath)
        return render_template('user/displayItem.html', email_info = email, eml_output = eml_output)

@user.route('/classify_email_<email_id>', methods=['GET', 'PUT'])
@login_required
def classify_email(email_id):
    case_id = int(request.form.get("case_id"))
    contact = request.form.get("contact")
    case_exists = get_case_by_caseId(case_id) #make sure that case_id exists

    user_id = current_user.UserId
    type_id = 2 #always "odpověď"
    email_info = get_email_by_emailId(email_id)
    sender = email_info['sender']
    reciever = "xx@gmail.com" 
    cc= None #dopln pozdejc
    if case_exists:
        new_item_from_email = create_case_item(case_id,type_id,sender,reciever,cc)
        item_id = new_item_from_email[0]
        if new_item_from_email:
            #change email state and move email file
            change_email_state(email_id, 30)
            new_filepath, new_filename, new_path = replace_email_file(email_id, item_id, case_id)
            #create new file form email in DB
            hashed_file = get_hashed_file(new_filepath)
            size = os.path.getsize(new_filepath)
            file_n, file_ext = os.path.splitext(new_filename)
            file_ext = file_ext.strip('.')
            new_case_file = create_file(item_id, new_path, file_n, file_ext, size, hashed_file)
            #create log
            text = "Email s ID {} byl úspěšně přirazen k případu ID {}".format(email_id, case_id)
            create_item_logs(item_id, user_id, text)
            #change case state
            if contact == 'Client':
                change_state_of_case(case_id, 60, user_id)
                state_id=60
            elif contact == 'Counterparty':
                state_id=100
                change_state_of_case(case_id, 100, user_id)

        return jsonify({"caseID": case_id, "stateID": state_id, "itemID": item_id})
    else:
        return "ERROR"



@user.route('/download_template')
@login_required
def downloadTemplate():
    filename = 'CZ_template.xlsx'
    path_to_template = os.path.join(current_app.config['DOWNLOAD_FOLDER'], filename)
    return send_file(path_to_template, as_attachment=True)

@user.route('/download_attachement/<eng_code>/<file>', methods=['GET', 'PUT'])
@login_required
def downloadAttachement(eng_code,file):
    uploadFolder =  get_settings('PathToFiles')[1]
    path_to_file = os.path.join(uploadFolder, eng_code, file ) # tohle pak ztahnout z DB!!
    return send_file(path_to_file, as_attachment=True)

@user.route('/change_email_state', methods=['GET', 'PUT'])
@login_required
def changeEmailState():
    email_id = int(request.form.get("email_id"))
    state_id = int(request.form.get("state_id"))
    result = change_email_state(email_id, state_id)
    return "OK"






