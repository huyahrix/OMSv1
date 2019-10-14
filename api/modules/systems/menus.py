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
from flask import request,jsonify,Response
from flask_api import status
import json
from .data.user import getUserMenu


class UserMenu(Resource):
    @jwt_required
    def get(self):
        if request.method == 'GET':
            user_id = get_jwt_identity()
            if not user_id :
                return {'status':'404','message':'user not found.'}, status.HTTP_404_NOT_FOUND
            data = getUserMenu(user_id)
        if not data:
           return {'status':'500','message':'Internal Server Error'}, status.HTTP_500_INTERNAL_SERVER_ERROR
           
        return jsonify(status=status.HTTP_200_OK,message='',data=data)