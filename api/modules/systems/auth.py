#  @copyright 2019 © DigiNet
#  @author Andy Trần Đào Anh
#  @create 2019/10/04 10:51
#  @update 2019/10/04 10:51

from flask import request,jsonify,Response
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
)
import json
from api.util.decrypt import decryptData
from api.util.blacklist import BLACKLIST
from .systems_data.user_data import getUserInfo,verifyPassword,listUser
#from api.util.encrypt import encrypt

BLANK_ERROR = "'{}' cannot be blank."
CREATED_SUCCESSFULLY = "User created successfully."
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
            # data = {"data": encrypt()}
            # print('hash: {}'.format(data))
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
                            access_token = create_access_token(identity=userData.user_id, fresh=True)
                            refresh_token = create_refresh_token(userData.user_id)
                            userInfo = {}
                            userInfo['userID'] = userData.user_id
                            userInfo['userName'] = userData.user_login_name
                            userInfo['departmentID'] = userData.group_id
                            userInfo['dateOfBirth'] = userData.emp_birth_date
                            userInfo['idCard'] = userData.emp_idcard_num
                            userInfo['height'] = userData.emp_height
                            userInfo['weight'] = userData.emp_weight
                            userInfo['currentAddress'] = (userData.emp_current_1_u + "," + userData.emp_current_2_u + "," + userData.emp_current_3_u)
                            userInfo['permanentAddress'] = (userData.emp_permanent_1_u + "," + userData.emp_permanent_2_u + "," + userData.emp_permanent_3_u)
                            userInfo['telephone'] = userData.emp_mobile
                            userInfo['officeExtention'] = userData.emp_pager
                            userInfo['hobbies'] = userData.emp_hobbies
                            response = jsonify(status = 200, message = "", sessionID = "0001", userInfo = userInfo, access_token = access_token, refresh_token = refresh_token)
                            response.status_code = status.HTTP_200_OK
                            return response
                        else:
                            return {'status': status.HTTP_404_NOT_FOUND, 'messsage': 'incorrect  password'}, 404
                    else:
                        return {'status': status.HTTP_404_NOT_FOUND, 'messsage': 'user not found'}, 404
                else:
                     return {'status': status.HTTP_400_BAD_REQUEST, 'messsage': 'cannot decrypt data'}, 400
            except:
                 return {'status': status.HTTP_400_BAD_REQUEST, 'messsage': ''}, 400


# Endpoint for revoking the current users access token
class Logout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        if not user_id:
            return {'status':'404','':''}, status.HTTP_404_NOT_FOUND
        BLACKLIST.add(jti)
        response = jsonify(status=status.HTTP_200_OK, message="User <id={}> successfully logged out.".format(user_id))
        response.status_code = status.HTTP_200_OK
        return response


# Standard refresh endpoint. A blacklisted refresh token
# will not be able to access this endpoint
class Refresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
