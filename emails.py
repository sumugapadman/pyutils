#!/opt/anaconda3/envs/pytuts/bin/python
import os
import base64
import email
import imaplib
from datetime import datetime, date, timedelta
from dotenv import load_dotenv

def getConfig():
    project_folder = os.getcwd()
    load_dotenv(os.path.join(project_folder, '.env'))
    return {
        "email_user" : os.getenv("USERNAME"),
        "email_pass" : os.getenv("PASSWORD"),
        "host" : os.getenv("HOST"),
        "port" : os.getenv("PORT")
    }
    
def connect():
    config = getConfig()
    email_user = config.get('email_user')
    email_pass = config.get('email_pass')
    host = config.get('host')
    port = config.get('port')
    mail = imaplib.IMAP4_SSL(host,port)
    mail.login(email_user, email_pass)
    return mail

def write_file(filename,data):
    if os.path.isfile(filename):
        with open(filename, 'a') as f:          
            f.write('\n' + data)   
    else:
        with open(filename, 'w') as f:                   
            f.write(data)

def mark_as_read():
    write_file('results.txt','====<<< Job Started : {0} >>>===='.format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
    mail = connect()
    readonly = False
    mail.select("INBOX", readonly)
    delta = int(os.getenv("DELTA"))
    curr_date = (date.today() - timedelta(delta)).strftime("%d-%b-%Y")
    type, data = mail.search(None, ('UNSEEN'), '(BEFORE {0})'.format(curr_date))
    mail_ids = data[0]
    id_list = mail_ids.split()
    write_file('results.txt','*** Processing {0} emails ***'.format(len(id_list)))
    for id in id_list:
        print('Marking email : {0} as read'.format(id))
        mail.store(id,'+FLAGS','\\SEEN')
    write_file('results.txt','====<<< Job Ended : {0} >>>===='.format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))

mark_as_read()