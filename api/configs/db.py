import os
import pyodbc as db
from api.configs.config  import config_by_name

ENV = os.environ.get("FLASK_ENV", "development")

server = config_by_name[ENV].DB_SERVER
database = config_by_name[ENV].DB_NAME
username = config_by_name[ENV].DB_USERNAME
password = config_by_name[ENV].DB_PASSWORD
connectionstring = config_by_name[ENV].DB_CONNECTIONSTRING
port = 1433
# list odbc driver
# for item in db.drivers():
#     print(item)

# driver = "ODBC Driver 17 for SQL Server"
driver = "ODBC Driver 13 for SQL Server" # centos 7
connectionstring = f'DRIVER={driver};SERVER={server};UID={username};PWD={password};DATABASE={database}'
print(connectionstring)

connection = db.connect(connectionstring)
cursor = connection.cursor()
