#!/usr/bin/env python3
import os
import base64
import email
import imaplib
import datetime
from dotenv import load_dotenv

def getConfig():
    project_folder = os.path.expanduser('~/Desktop/Workspace/pyutils')
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

def mark_as_read():
    mail = connect()
    readonly = False
    mail.select("INBOX", readonly)
    delta = int(os.getenv("DELTA"))
    date = (datetime.date.today() - datetime.timedelta(delta)).strftime("%d-%b-%Y")
    type, data = mail.search(None, ('UNSEEN'), '(BEFORE {0})'.format(date))
    mail_ids = data[0]
    id_list = mail_ids.split()
    print(len(id_list))
    for id in id_list:
        print(id)
        mail.store(id,'+FLAGS','\\SEEN')
    print('*** Marked {0} emails as Read'.format(len(id_list)))

mark_as_read()