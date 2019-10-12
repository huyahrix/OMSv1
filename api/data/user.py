from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
import pyodbc 
import bcrypt
from api.configs.db import cursor

def getUserInfo(userName):
	#strSQL = "select * from users where user_login_name LIKE '{userName}' and status = 0".format(userName=userName)
    strSQL ="""SELECT * from users 
    INNER JOIN  employees ON user_id = emp_id 
    LEFT JOIN mailgroup ON director_emp_id = emp_id 
    WHERE user_login_name LIKE '{userName}' and status = 0 """.format(userName=userName)
    cursor.execute(strSQL)
    row = cursor.fetchone()
    return row


def verifyPassword(password, dbHash):
	if bcrypt.checkpw(password.encode("utf8"), dbHash.encode("utf8")):
	    return True
	else:
	    return False