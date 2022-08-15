import psycopg2
import mysql.connector

import os

import json

files_dir = os.path.join(os.getcwd(),"credential","credentials.json")

f = open(files_dir)
  
# returns JSON object as 
# a dictionary
data = json.load(f)
print(data)

# print(data['dest_credential'])
# print(data['src_credential'])
try:
    # dwh
    database = data['dest_credential']["database"]
    user = data['dest_credential']["user_name"]
    password = data['dest_credential']["password"]
    host = data['dest_credential']["host"]
    port = data['dest_credential']["port"]
    #destination database
    dsestination_db_conn = psycopg2.connect(database = database,
                                    user = user,
                                    password = password,
                                    host= host,
                                    port = port,
                                    
                                    )
   
    

    # dsestination_db_cursor = dsestination_db_conn.cursor()



    src_db_conn = mysql.connector.connect(
                        host= data['src_credential']["host"],
                        user= data['src_credential']["user_name"],
                        database= data['src_credential']["database"],
                        port = data['src_credential']["port"],
                        password=data['src_credential']["password"]
                        )

    user_mail = data["mail_credential"]["user_mail"]
    password = data["mail_credential"]["mail_app_password"]
    to_receiver = data["mail_credential"]["to_receiver"]
    CC_receivers = data["mail_credential"]["CC_receivers"]

    print("success")
except:
    print("failed")