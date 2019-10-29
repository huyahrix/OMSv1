#  @copyright 2019 © DigiNet
#  @author ahrix<infjnite@gmail.com>
#  @create 2019/10/04 10:51
#  @update 2019/10/04 10:51

from flask import request,jsonify,Response,make_response
from flask_api import status
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
    decode_token
)
from datetime import datetime 
import time   
import json
from api.util.decrypt import decryptData
from api.util.encrypt import encrypt
from api.util.blacklist_helpers import (
    is_token_revoked, add_token_to_database, get_user_tokens,
    revoke_token, unrevoke_token,
    prune_database
)
from api.resources.system import getUserInfo, verifyPassword, CreateSessions, GetSesionID

BLANK_ERROR =          "'{}' cannot be blank."
CREATED_SUCCESSFULLY = "User created successfully."
USER_NOT_FOUND =       "invalid username or password"
INCORRECT_PASWORD =    "invalid username or password"
CANNOT_DECRYPT_DATA =  "Cannot decrypt data"
SERVICE_UNAVAILABLE =  "Service Unavailable"

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    "username", type=str, required=True, help=BLANK_ERROR.format("username")
)
_user_parser.add_argument(
    "password", type=str, required=True, help=BLANK_ERROR.format("password")
)

# Login endpoint
class Login(Resource):
    def post(self):
        if request.method == 'POST':
            data = request.get_json()
            #data = {"data": encrypt()}
            #print('hash: {}'.format(data))
            try:
                plainText = decryptData(data['data'])
                if plainText:
                    # print(plainText)
                    objLog = json.loads(plainText)
                    attemptUserName = objLog['username']
                    attemptPassword = objLog['password']
                    userData = getUserInfo(attemptUserName)
                    if userData:
                        if verifyPassword(attemptPassword, userData.user_login_password):
                             # Create our JWTs
                            access_token = create_access_token(identity=userData.user_id, fresh=True)
                            refresh_token = create_refresh_token(userData.user_id)
                             # Store the tokens in our store with a status of not currently revoked.
                            add_token_to_database(access_token, 'identity')
                            add_token_to_database(refresh_token, 'identity')
                            # user info
                            userInfo = {}
                            userInfo['userID'] = userData.user_id
                            userInfo['userName'] = userData.user_login_name
                            userInfo['departmentID'] = userData.group_id
                            userInfo['dateOfBirth'] = userData.emp_birth_date.strftime('%Y-%m-%d %H:%M:%S')
                            userInfo['idCard'] = userData.emp_idcard_num
                            userInfo['height'] = userData.emp_height
                            userInfo['weight'] = userData.emp_weight
                            userInfo['currentAddress'] = (userData.emp_current_1_u + "," + userData.emp_current_2_u + "," + userData.emp_current_3_u)
                            userInfo['permanentAddress'] = (userData.emp_permanent_1_u + "," + userData.emp_permanent_2_u + "," + userData.emp_permanent_3_u)
                            userInfo['telephone'] = userData.emp_mobile
                            userInfo['officeExtention'] = userData.emp_pager
                            userInfo['hobbies'] = userData.emp_hobbies
                            # data 
                            decoded_access_token = decode_token(access_token)
                            decoded_refresh_token = decode_token(refresh_token)
                            data = {}
                            data['access_token_id'] = decoded_access_token['jti']
                            data['access_token_createdAt'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            data['access_token_updatedAt'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            data['access_token_expiredAt'] = datetime.fromtimestamp(decoded_access_token['exp']).strftime('%Y-%m-%d %H:%M:%S')
                            data['refresh_token_id'] = decoded_refresh_token['jti']
                            data['refresh_token_createdAt'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            data['refresh_token_updatedAt'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            data['refresh_token_expiredAt'] = datetime.fromtimestamp(decoded_refresh_token['exp']).strftime('%Y-%m-%d %H:%M:%S')
                            # create session
                            session = {}
                            old_session = GetSesionID()
                            if old_session:
                                session_id = int(old_session.SessionID) + 1
                            else:
                                session_id = str(int(datetime.now().year) * 10000 + int(datetime.now().month) * 100 + int(datetime.now().day)) + '00000'
                            session['SessionID'] = session_id
                            session['UserID'] = userData.user_id
                            session['DateTimeLogin'] = time.strftime('%Y-%m-%d %H:%M:%S')
                            session['IPAddress'] = request.remote_addr
                            session['ServerID'] = 'B'
                            if CreateSessions(session):
                                return make_response(jsonify(status = 200, msg = "", sessionID = session['SessionID'], userInfo = userInfo, access_token = access_token, refresh_token = refresh_token,data=data),200)
                            else:
                                return make_response(jsonify(status=400,msg=''),400)
                        else:
                            return make_response(jsonify(status=404,msg=INCORRECT_PASWORD),404)
                    else:
                        return make_response(jsonify(status=404,msg=USER_NOT_FOUND),404)
                else:
                     return make_response(jsonify(status=400,msg=CANNOT_DECRYPT_DATA),400)
            except:
                return make_response(jsonify(status=400,msg=''),400)


# Endpoint for revoking the current users access token
class Logout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        if not user_id:
            return make_response(jsonify(status=404, msg=USER_NOT_FOUND),404)
        # BLACKLIST.add(jti)
        if not revoke_token(jti,user_id):
            return make_response(jsonify(status=503,msg=''),503) 
        return make_response(jsonify(status=status.HTTP_200_OK, msg="User <id={}> successfully logged out.".format(user_id)),200)


# Check token
# 
class Check(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        try:
            decoded_access_token = get_raw_jwt()
            token_id = decoded_access_token['jti']
            data = get_user_tokens(token_id)
            response_data = {}
            response_data['access_token_id'] = data.token_id
            response_data['access_token_createdAt'] = data.createAt
            response_data['access_token_updatedAt'] = data.updateAt
            response_data['access_token_expiredAt'] = data.expiresAt
            return make_response(jsonify(status = 200,msg='',data=response_data), 200)
        except:
           return make_response(jsonify(status=400,msg='Bad request'),400)


# Standard refresh endpoint. A blacklisted refresh token
# will not be able to access this endpoint
class Refresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        try:
            if not add_token_to_database(new_token, 'identity'):
                return make_response(jsonify(status = 503,msg=SERVICE_UNAVAILABLE,data=''),503)
            decoded_access_token = decode_token(new_token)
            data = {}
            data['access_token_id'] = decoded_access_token['jti']
            data['access_token_createdAt'] = datetime.now()
            data['access_token_updatedAt'] = datetime.now()
            data['access_token_expiredAt'] = datetime.fromtimestamp(decoded_access_token['exp'])
            return make_response(jsonify(status = 200,msg='',access_token=new_token,data=data), 200)
        except:
            return make_response(jsonify(status=400,msg='Bad request'),400)


class ModifyToken(Resource):
    @jwt_required
    def put(self, token_id):
        # Get and verify the desired revoked status from the body
        json_data = request.get_json(silent=True)
        if not json_data:
            return make_response(jsonify(status=400, msg="Missing 'revoke' in body"), 400)
        revoke = json_data.get('revoke', None)
        if revoke is None:
            return make_response(jsonify(status=400, msg="Missing 'revoke' in body"), 400)
        if not isinstance(revoke, bool):
            return make_response(jsonify(status=400,msg="'revoke' must be a boolean"), 400)

        # Revoke or unrevoke the token based on what was passed to this function
        user_identity = get_jwt_identity()
        try:
            if revoke:
                revoke_token(token_id, user_identity)
                return make_response(jsonify(status=200, msg='Token revoked'), 200)
            else:
                unrevoke_token(token_id, user_identity)
                return make_response(jsonify(status=200, msg='Token unrevoked'), 200)
        except:
            return make_response(jsonify(status=404, msg='The specified token was not found'), 404)