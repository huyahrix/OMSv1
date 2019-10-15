import logging,sys,os
import pyodbc as db
from api.configs.flask_config  import config_by_name

ENV = os.environ.get("FLASK_ENV", "development")

server = config_by_name[ENV].DB_SERVER
database = config_by_name[ENV].DB_NAME
username = config_by_name[ENV].DB_USERNAME
password = config_by_name[ENV].DB_PASSWORD
connectionstring = config_by_name[ENV].DB_CONNECTIONSTRING
port = 1433

# list pyodbc driver
# for item in db.drivers():
#     print(item)

if bool("win" in sys.platform):
    driver = "ODBC Driver 17 for SQL Server"
else:
    driver = "ODBC Driver 13 for SQL Server" # centos 7
connectionstring = f'DRIVER={driver};SERVER={server};UID={username};PWD={password};DATABASE={database}'
print(' * {str}'.format(str=connectionstring))
connection = db.connect(connectionstring)
cursor = connection.cursor()