""" send sms """
import time
import math
import random
import datetime
from django.db import connection
from django.conf import settings

import os
import requests
import multiprocessing as mp
from time import sleep
import hashlib
import sms




#set dhjango settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "script_settings")
""" if your are getting this error:
Commands out of sync; you can't run this command now, 

soln: run single sql statments per cursor

if lock timeout exceeded, make sure you commit after running the for update clause in select
"""
    
""" settings """

PROFILE_NAME='ujumbe'

      
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
    
def dictfetchone(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, cursor.fetchone()))

def get_outgoing_sms(cursor):
    cursor.execute("SELECT * FROM  notifications_message WHERE message_status=0 and message_type=2")
    return dictfetchall(cursor)


def update_outgoing_sms(cursor,id):
    cursor.execute("UPDATE notifications_message SET message_status=1 WHERE id=%s \
    "%(id))
    return cursor.rowcount



def run():
    while True:
        cursor=connection.cursor()
        
        messages=get_outgoing_sms(cursor)
        cursor.close() 
        
   
        #send sms
        for message in messages:
            try:
                cursor=connection.cursor()
                print ("Sending sms")
                reply=sms.send("twilio","+"+message.get('recipient_address'), message.get("message"))
                #save to db
                update_outgoing_sms(cursor,message.get('id'))
                print ("sent")
                

            except:
                pass
            finally:
                cursor.close() 



        sleep(2)
        
#runs
run()
    
