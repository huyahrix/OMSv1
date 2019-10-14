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
# driver = {[x for x in db.drivers() if x.endswith('17 for SQL Server')][0]}
# driver = db.drivers()
print("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
for item in db.drivers():
    print(item)


# driver = [item for item in db.drivers()][-1]
driver = "ODBC Driver 17 for SQL Server"
print(driver)
connectionstring = f'DRIVER={driver};SERVER={server};UID={username};PWD={password};DATABASE={database}'
print(connectionstring)

connection = db.connect(connectionstring)
cursor = connection.cursor()
