from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker, ActionExecutionRejection
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
import requests
import json
import yaml
import re
# email libraries
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders
# from email.message import EmailMessage
# from time import sleep
# mysql db libraries
import mysql.connector
import logging
from datetime import datetime
logger = logging.getLogger(__name__)

with open('actions/appConfig.yml') as test:
    val = yaml.safe_load(test)

# def check_claim_id_uniqueness(claim_id: Text):
#     print("Checking Claim ID uniqueness")
#     cnx = mysql.connector.connect(**val['db'])
#     cursor = cnx.cursor(buffered=True)
#     query = "select claimId from users where claimId=%s;" # change query according to new schema
#     details = claim_id
#     cursor.execute(query,(details,))
#     print(f"cursor.rowcount: {cursor.rowcount}")
#     print(f"cursor.execute:{cursor.execute}")
#     if cursor.rowcount == 1:
#         result = 0
#     else:
#         result = 1
#     logger.debug(cursor.rowcount)
#     print(f"cursor.statement:{cursor.statement}")
#     cursor.close()
#     cnx.close()
#     print(f"result:{result}")
#     return result

# def fetch_all_slots_from_db(claim_id: Text):
#     print("Fetching details from db...")
#     cnx = mysql.connector.connect(**val['db'])
#     cursor = cnx.cursor(buffered=True)
#     query = "select userFirstName, userLastName, NPI, updatedDate from users where claimId=%s;" # change query accorfing to new schema
#     details = claim_id
#     cursor.execute(query,(details,))
#     result_set = cursor.fetchone()
#     result_set = list(result_set)
#     cursor.close()
#     cnx.close()
#     current_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
#     current_date = datetime.strptime(current_date,'%Y-%m-%d %H:%M:%S')
#     diff = current_date - result_set[3]
#     print(f"Difference in hours:{diff.total_seconds()/3600}")
#     if (diff.total_seconds()/3600 < 12): 
#         result_set.append("1")
#     else:
#         result_set.append("0")
#     print(f"Result set:{result_set}")
#     return result_set

def check_local_db(id, npi, category):
    cnx = mysql.connector.connect(**val['db'])
    cursor = cnx.cursor(buffered=True)
    query = "select u.userFirstName,u.userLastName,uce.updatedDate from users u inner join user_category_entity \
              uce on u.userId = uce.userId where uce.uniqueIdentifier=%s and uce.categoryId=%s and u.NPI=%s;"
    details = (id,category,npi)
    cursor.execute(query,details)
    fetched_details = cursor.fetchone()
    cursor.close()
    cnx.close()
    if fetched_details:
        in_db = 1
        fetched_details = list(fetched_details)
        current_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        current_date = datetime.strptime(current_date,'%Y-%m-%d %H:%M:%S')
        diff = current_date - fetched_details[2]
        if (diff.total_seconds()/3600 < 12):
            fetched_details.append("recent")
        else:
            fetched_details.append("not_recent")
    else:
        in_db = 0
        fetched_details = []
    return in_db,fetched_details

def store_user_details(providerFirstName, providerLastName, providerNpi, claimId, category):
    cnx = mysql.connector.connect(**val['db'])
    cursor = cnx.cursor(buffered=True)
    x = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    updated_date = datetime.strptime(x,"%Y-%m-%d %H:%M:%S")

    check_old_user_query = "select userId from users where NPI = %s;"
    old_user_query_params = providerNpi
    cursor.execute(check_old_user_query,(old_user_query_params,))
    isOldUser = cursor.fetchone()
    if isOldUser:
        isOldUser = list(isOldUser)
        check_combination_query = "select userId from user_category_entity where userId = %s\
                                     and uniqueIdentifier = %s and categoryId = %s;"
        combination_query_params = (isOldUser[0],claimId,category)
        cursor.execute(check_combination_query,combination_query_params)
        combination_exist = cursor.fetchone()
        if combination_exist:
            update_query = "update user_category_entity set updatedDate=%s where uniqueIdentifier = %s\
                         and categoryId = %s and userId = %s;"
            update_query_params = (updated_date,claimId,category,isOldUser[0])
            try:
                cursor.execute(update_query,update_query_params)
                cnx.commit()
            except:
                print("Couldn't update the users table column!")
        else:
            insert_identifier_query = "insert into user_category_entity\
                            (userId,categoryId,uniqueIdentifier,updatedDate) values(%s,%s,%s,%s);"
            insert_id_query_params = (isOldUser[0],category,claimId,updated_date)
            try:
                cursor.execute(insert_identifier_query,insert_id_query_params)
                cnx.commit()
            except:
                print("Couldn't insert into category entity table!")
    else:
        insert_user_details_query = "insert into users (userFirstName,userLastName,NPI)\
                                 values(%s,%s,%s);"
        insert_user_query_params = (providerFirstName,providerLastName,providerNpi)
        try:
            cursor.execute(insert_user_details_query,insert_user_query_params)
            cnx.commit()
        except:
            print("Couldn't insert into users table!")
        
        insert_identifier_query = "insert into user_category_entity (userId,categoryId,uniqueIdentifier,updatedDate)\
                values((select userId from users where NPI=%s),%s,%s,%s);"
        insert_id_query_params = (providerNpi,category,claimId,updated_date)
        try:
            cursor.execute(insert_identifier_query,insert_id_query_params)
            cnx.commit()
        except:
            print("Couldn't insert into category entity table!")

    logger.debug(cursor.rowcount)
    cursor.close()
    cnx.close()
    return []
 
# def check_local_db(id, npi, category):
#     a = check_claim_id_uniqueness(id)
#     b = fetch_all_slots_from_db(id)
#     print(a, b) 
#     return a, b
#     # return check_claim_id_uniqueness(claim_id), fetch_all_slots_from_db(claim_id)