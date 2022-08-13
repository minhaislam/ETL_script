#ETL Assignment Guideline

## Step 1: Ingesting Dummy Data in Mysql DB

- First Downloaded the dummy data from a website. (https://www.mysqltutorial.org/mysql-sample-database.aspx)
- The sql file can be found in

>- sql_flies folder
>- File name **mysqlsampledatabase.sql**

- execute the in a IDE to create table and data. The name of the database will be **classicmodels**

## Step 2: Create Corresponding table for ETL in Postgres DB

- The sql file can be found in

>- sql_flies folder
>- File name **postgres_db_ddl.sql**

- All the DDL for the table are given there
- Also added a log table in order to keep track of the Script.


## Step 3: Writing ETL framework (Using Python)

- First create a folder
- Open command line and run **pipenv shell**
- If pipenv not installed then install the librery using pip and then run the command
```sh
pip install pipenv
```
- After creating virtual environment install all the libreries by running
```sh
pip install -r requirements.txt
```

## How the ETL works
- There is a file in **credential** folder

```sh
{
    "src_credential":{
        "database":"",
        "host":"",
         "port":,
        "user_name": "",
        "password": ""
    },
    
    "dest_credential":{
        "database":"",
        "host":"",
         "port":,
        "user_name": "",
        "password": ""
    },
    "mail_credential":{
        "user_mail":"",
        "mail_app_password": ""
        "to_user":"minhajislam95@gmail.com",
        "CC_user":[""]
    }

}
```

- It contains Json data where source and destination credentials needs to be inserted
- Also credentials for sending mail needs to be provided.
- In mail_app_password section user's passord or app_password can be given

- There is another json file named **table_names.json**

```sh
{
    "src_DB_name":"",
    "src_table_name":"",
    "src_target_column":"",
    "dest_schema_name":"",
    "dest_table_name":"",
    "dest_target_column":"",
    "status":""
}
```
- This file contains multiple json. One can add or remove json from this file. if necessary.
- It contains iformation on how to access source table and how to access destination tables.
- The status are two type 'active'/'inactive'. Only tables having active status will fetch data from source and insert in destination.

- [Mail System] - Mail system is used to alert corresponding people after ETL process is fininsd with a log file.
- [Log File] - The log file contains how many data were inserted on that specific hour.

## Step 4: Setting up hourly cromjob in Crontab(OS: centos 7)
- move the ETL scriptin a directory
- Login as a root user and install python and other corresponding libreries from requirements.txt
- Install cron if not installed.
```sh
yum -y install cron
```
- Install cron if not installed.
- To edit cron write:
```sh
crontab -e
```
- Configure the cron file. Inside cron file write:
```sh
00 0-23 * * * python_file_location loaction_of_script/main.py 
example:
00 0-23 * * * bin/python3 ETL_script/main.py 
```
- Here **00 0-23** means the script will run in the first minute of every hour.
- to get python location run 
```sh
which python
```

## Step 5: Adding a BI tool to the Data warehouse (Power BI)
- Download and Install power BI from microsoft store
- Click on files-> Get Data->Get Data to get started
- select postgres database from the list
- Fillup the required fields to connect to data source
- Finally select necessary tables and load them