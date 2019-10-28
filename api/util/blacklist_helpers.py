from datetime import datetime
from flask_jwt_extended import decode_token
from api.util.exceptions import TokenNotFound
from api.configs.db import cursor,cnxn 
import pyodbc,logging


def _epoch_utc_to_datetime(epoch_utc):
    """
    Helper function for converting epoch timestamps (as stored in JWTs) into
    python datetime objects (which are easier to use with sqlalchemy).
    """
    return datetime.fromtimestamp(epoch_utc)


def add_token_to_database(encoded_token, identity_claim):
    """
    Adds a new token to the database. It is not revoked when it is added.
    :param identity_claim:
    """
    decoded_token = decode_token(encoded_token)
    jti = decoded_token['jti']
    token_type = decoded_token['type']
    user_identity = decoded_token[identity_claim]
    expires = _epoch_utc_to_datetime(decoded_token['exp'])
    revoked = 0
    currenttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    str_query = """INSERT INTO token_blacklist (token_id, token_type, user_identity, revoked, createAt, updateAt, expiresAt)
    VALUES ('{jti}', '{token_type}', '{user_identity}', '{revoked}','{createAt}','{updateAt}','{expiresAt}');""".format(jti=jti,
                                                                                             token_type=token_type,
                                                                                             user_identity=user_identity,
                                                                                             revoked=revoked,
                                                                                             createAt = currenttime,
                                                                                             updateAt = currenttime,
                                                                                             expiresAt= expires)
    try:
        cursor.execute(str_query)
        cnxn.commit()
        return True
    except pyodbc.Error as ex:
        logging.error(ex.args[1])
        return False


def is_token_revoked(decoded_token):
    """
    Checks if the given token is revoked or not. Because we are adding all the
    tokens that we create into this database, if the token is not present
    in the database we are going to consider it revoked, as we don't know where
    it was created.
    """
    jti = decoded_token['jti']
    try:
        str_query="""SELECT revoked 
        FROM token_blacklist 
        WHERE token_id ='{}'""".format(jti)
        cursor.execute(str_query)
        result = cursor.fetchone()
        if result.revoked == 1:
            return True
        return False
    except:
        if not pyodbc.Error:
            logging.error(pyodbc.Error.args[1])
        return False


def get_user_tokens(token_id):
    """
    Returns all of the tokens, revoked and unrevoked, that are stored for the
    given user
    """
    sql_query="SELECT * FROM token_blacklist WHERE token_blacklist.token_id = '{}' ".format(token_id)
    try:
        cursor.execute(sql_query)
        result = cursor.fetchone()
        #data = [dict(zip([key[0] for key in cursor.description], row)) for row in result]
        return result
    except pyodbc.Error as ex:
        logging.error(ex.args[1])
        return None


def revoke_token(token_id, user):
    """
    Revokes the given token. Raises a TokenNotFound error if the token does
    not exist in the database
    """
    try:
        sql_query = """UPDATE token_blacklist
        SET revoked = 1
        WHERE token_id = '{token_id}' AND user_identity = '{user}' ;""".format(token_id=token_id,user=user)
        cursor.execute(sql_query)
        cnxn.commit()
        return True
    except pyodbc.Error as ex:
        logging.error(ex.args[1])
        return False


def unrevoke_token(token_id, user):
    """
    Unrevokes the given token. Raises a TokenNotFound error if the token does
    not exist in the database
    """
    try:
        sql_query = """UPDATE token_blacklist
        SET revoked = 0
        WHERE token_id = '{token_id}' AND user_identity = '{user}';""".format(token_id=token_id,user=user)
        cursor.execute
        cnxn.commit()
    except pyodbc.Error as ex:
        logging.error(ex.args[1])


def prune_database():
    """
    Delete tokens that have expired from the database.

    How (and if) you call this is entirely up you. You could expose it to an
    endpoint that only administrators could call, you could run it as a cron,
    set it up with flask cli, etc.
    """
    now = datetime.now()
    sql_query="DELETE FROM products WHERE expiresAt < '{}'".format(now)
    cursor.execute(sql_query)
    cnxn.commit()
