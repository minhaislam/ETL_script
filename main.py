import json
from DB_connection import src_db_conn,dsestination_db_conn,user_mail,password,to_receiver,CC_receivers
import psycopg2.extras
import math
import pandas as pd
from os.path import dirname,abspath
import os
from pretty_html_table import build_table
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def fetch_max_id_src_table(v_src_db_name,v_src_table_name,v_src_tgt_column,v_src_db_cursor):
    sql = f"SELECT coalesce(cast(max({v_src_tgt_column}) as int),0) FROM {v_src_db_name}.{v_src_table_name};"    
    v_src_db_cursor.execute(sql)   
    max_id = v_src_db_cursor.fetchone()
    return max_id


def fetch_max_id_dest_table(v_dest_schema_name,v_dest_table_name,v_dest_tgt_colum,v_dest_db_cursor):
    sql = f"SELECT coalesce(max({v_dest_tgt_colum}::int4),0) FROM {v_dest_schema_name}.{v_dest_table_name};"  
    v_dest_db_cursor.execute(sql)   
    max_id_2 = v_dest_db_cursor.fetchone()
    return max_id_2


def get_dest_table_datatypes(v_tables_names,v_dest_schema_name,v_dsestination_db_cursor):
    sql_query_column_data_type= f'''               
                                                
                                        select
                                column_name,
								udt_name 
                            from
                                information_schema.columns
                            where
                                table_schema = '{v_dest_schema_name}'
                                and table_name = '{v_tables_names}';
                                
                                                '''
                

    v_dsestination_db_cursor.execute(sql_query_column_data_type)
    table_info = v_dsestination_db_cursor.fetchall()

    # print(table_info)
    field_names = [i[0] for i in table_info]
    field_data_type = [i[1] for i in table_info]

    v_field_namess = ', '.join(field_names)

    v_data_type_str = [f'%s::{field_data_type[i]}' for i in range(len(field_names))]
    v_data_type = ', '.join(v_data_type_str)
    return [v_field_namess,v_data_type]
    # pass

def insert_to_dwh(v_new_rows,v_schema_name_dest,v_table_name_dest,v_dest_table_datatype,v_dsestination_db_conn,v_dsestination_db_cursor):

    insert_string = f'''insert into {v_schema_name_dest}.{v_table_name_dest} ({v_dest_table_datatype[0]}) values ({v_dest_table_datatype[1]}) ''';
    print(insert_string)

    psycopg2.extras.execute_batch(v_dsestination_db_cursor,insert_string,v_new_rows)
    v_dsestination_db_conn.commit()
    
    # pass

def insert_to_log_table(v_log_data,v_dsestination_db_conn,v_dsestination_db_cursor):

    insert_string = f'''INSERT INTO public.data_etl_log
                                    (table_name, row_count, data_insertion_time)
                                    VALUES('{v_log_data[0]}', '{str(v_log_data[1])}', now());''';
    print(insert_string)

    # psycopg2.extras.execute_batch(v_dsestination_db_cursor,insert_string)
    v_dsestination_db_cursor.execute(insert_string)
    v_dsestination_db_conn.commit()


def mail_data(v_get_log,v_user_mail,v_password,to_receiver,CC_receivers):

    sumamry_df = pd.DataFrame(v_get_log,columns=["Table Name", "No of Row Inserted"])  
    output = build_table(sumamry_df, 'grey_light')
    print(sumamry_df)

    message = MIMEMultipart()
    message['Subject'] = 'ETL Job Alert'
    message['From'] = f'{v_user_mail}'
    # To_receiver = ['minhajul.islam@surecash.net']
    To_receiver = [f'{to_receiver}']
    # Cc_receiver  =['minhajul.islam@surecash.net']
    Cc_receiver  =CC_receivers
    message['To']=";".join(To_receiver)
    message['Cc']=";".join(Cc_receiver)
    receiver = To_receiver + Cc_receiver

    body_content = output
    body = '''
            Assalamualaikum,<br>
            <br>

        The log for Last hours ETL<br>
            
        "<br>

            '''+body_content+'''


        <br>
        Regards,<br>
        Name:<br>
        Designation: 
            '''
    
    message.attach(MIMEText(body, "html"))


    msg_body = message.as_string()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(message['From'], f'{v_password}')
    server.sendmail(message['From'], receiver, msg_body)
    server.quit()
    print('Mail Sent')

    # return "Mail sent successfully."



def fail_mail_data(v_get_error_log,v_user_mail,v_password,to_receiver,CC_receivers):


    message = MIMEMultipart()
    message['Subject'] = 'ETL Job Fail Alert'
    message['From'] = f'{v_user_mail}'
    # To_receiver = ['minhajul.islam@surecash.net']
    To_receiver = [f'{to_receiver}']
    # Cc_receiver  =['minhajul.islam@surecash.net']
    Cc_receiver  =CC_receivers
    message['To']=";".join(To_receiver)
    message['Cc']=";".join(Cc_receiver)
    receiver = To_receiver + Cc_receiver

    body = '''
            Assalamualaikum,<br>
            <br>

        The Last hours ETL failed.<br>
            
        "<br>

            '''+str(v_get_error_log)+'''


        <br>
        Regards,<br>
        Name:<br>
        Designation: 
            '''
    
    message.attach(MIMEText(body, "html"))


    msg_body = message.as_string()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(message['From'], f'{v_password}')
    server.sendmail(message['From'], receiver, msg_body)
    server.quit()
    print('Mail Sent')



# Registered:
def main(v_tables_names_json,v_src_db_conn,src_db_cursor,v_dsestination_db_conn,dsestination_db_cursor):
    get_log =[]
    for table_names_json in v_tables_names_json:
        if table_names_json['status'] == 'active':
            # print(table_names_json)
    
            min_value = fetch_max_id_dest_table(table_names_json["dest_schema_name"],table_names_json["dest_table_name"],table_names_json["dest_target_column"],dsestination_db_cursor)
            max_value =fetch_max_id_src_table(table_names_json["src_DB_name"],table_names_json["src_table_name"],table_names_json["src_target_column"],src_db_cursor)
            
            print(f'Src Table : {table_names_json["src_table_name"]} to Dest Table : {table_names_json["dest_table_name"]}')
            print(f"min value: {min_value[0]} ------> max value: {max_value[0]}")

            v_dest_table_datatypes=get_dest_table_datatypes(table_names_json["dest_table_name"],table_names_json["dest_schema_name"],dsestination_db_cursor)
            log_tuple = (f'{table_names_json["src_table_name"]}', f'{max_value[0]-min_value[0]}')
            print(log_tuple)
            get_log.append(log_tuple)
            print(f'data log: {log_tuple}')
            if max_value[0]> min_value[0]:

                start_index = min_value[0]
                v_add_range = 5000
                end_index = start_index+v_add_range
                max_id_value_diff = max_value[0]-start_index
                range_value = math.ceil(max_id_value_diff/v_add_range)
                # print(max_id_value_diff)

                for i in range(0,range_value):

                    sql_query_to_dump= f'''               
                                                        
                                        select
                                            * 
                                from {table_names_json["src_DB_name"]}.{table_names_json["src_table_name"]} e where {table_names_json["src_target_column"]} > {str(start_index)} and {table_names_json["src_target_column"]} <= {str(end_index)}'''
                                                        
                        

                    src_db_cursor.execute(sql_query_to_dump)
                    new_rows = src_db_cursor.fetchall()
                    print(sql_query_to_dump)

                    # field_names = [i[0] for i in src_db_cursor.description]
                

                    insert_to_dwh(new_rows,table_names_json["dest_schema_name"],table_names_json["dest_table_name"],v_dest_table_datatypes,v_dsestination_db_conn,dsestination_db_cursor)

                    insert_to_log_table(log_tuple,v_dsestination_db_conn,dsestination_db_cursor)
                    start_index = end_index
                    end_index = end_index+v_add_range
            else:
                insert_to_log_table(log_tuple,v_dsestination_db_conn,dsestination_db_cursor)
                print('no data to fetch')
    return get_log


if __name__ == '__main__':
    try:

        src_db_cursor = src_db_conn.cursor()

        dsestination_db_cursor = dsestination_db_conn.cursor()
        config_table_dir = os.path.join(dirname(abspath(__file__)),"table_names.json")

        f = open(config_table_dir)
        
        # returns JSON object as 
        # a dictionary
        table_names = json.load(f)
        v_log = main(table_names,src_db_conn,src_db_cursor,dsestination_db_conn,dsestination_db_cursor)

        mail_data(v_log,user_mail,password,to_receiver,CC_receivers)
    except Exception as e:
        fail_mail_data(e,user_mail,password,to_receiver,CC_receivers)
