import logging
import pyodbc 
import bcrypt
import json
from api.configs.db import cursor, cnxn


def getUserInfo(userName):
	#strSQL = "select * from users where user_login_name LIKE '{userName}' and status = 0".format(userName=userName)
    strSQL ="""SELECT * from users 
    INNER JOIN  employees ON user_id = emp_id 
    LEFT JOIN mailgroup ON director_emp_id = emp_id 
    WHERE user_login_name LIKE '{userName}' and status = 0 """.format(userName=userName)
    try:
        cursor.execute(strSQL)
        resuft = cursor.fetchone()
        return resuft
    except pyodbc.Error as ex:
        logging.error(ex.args[1])
        return None
    


def getUserMenu(userId):
    strSQL="""select [g].[module_group_id], [g].[module_group_name] as [module_group], 
    [f].[module_id], [m].[module_name], [m].[module_icon], [m].[module_display_order], [f].[menu_id] as [form_id], [f].[menu_name] as [form_name], 
    [f].[menu_icon] as [form_icon], [f].[menu_display_order], [f].[url], 
    CASE WHEN b.menu_id IS NULL THEN 0 ELSE 1 END AS bookmark, 
    CASE WHEN B.menu_id IS NULL THEN 'fa fa-star-o text-green' ELSE 'fa fa-star text-grey' END AS bookmark_icon, 
    [g].[display_order], [f].[is_old_menu], [f].[old_permission], [f].[disabled], [f].[checkPermissions], [f].[form_active] 
    from [MainMenu] as [f] 
    left join [module] as [m] on [m].[module_id] = [f].[module_id] 
    left join [module_group] as [g] on [g].[module_group_id] = [m].[module_group_id] 
    left join [bookmarkmenu] as [b] on [b].[menu_id] = [f].[menu_id] and [b].[user_id] = '{user_id}' 
    where [f].[disabled] = '0' and [f].[is_menu] = '1' 
    order by g.display_order, m.module_display_order, f.menu_display_order""".format(user_id = userId)
    try:
        cursor.execute(strSQL)
        result = cursor.fetchall()
        data = [dict(zip([key[0] for key in cursor.description], row)) for row in result]
        return data
    except pyodbc.Error as ex:
        logging.error(ex.args[1])
        return None
    


def verifyPassword(password, dbHash):
	if bcrypt.checkpw(password.encode("utf8"), dbHash.encode("utf8")):
	    return True
	else:
	    return False

def getCustomizeMenu(userId):
    strSQL = """select * from [customize_bookmark_menu] where [user_id] = '{}'""".format(userId)
    try:
        cursor.execute(strSQL)
        result = cursor.fetchall()
        data = [dict(zip([key[0] for key in cursor.description], row)) for row in result]
        return data
    except pyodbc.Error as ex:
        logging.error(ex.args[1])
        return None