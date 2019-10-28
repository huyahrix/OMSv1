#  @copyright 2019 © DigiNet
#  @author ahrix<infjnite@gmail.com>
#  @create 2019/10/04 10:51
#  @update 2019/10/14 10:51

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
from flask import request,jsonify,Response, make_response
from flask_api import status
import json
from api.resources.system import getUserMenu


class Side_navigation_menu(Resource):
    @jwt_required
    def get(self):
        if request.method == 'GET':
            user_id = get_jwt_identity()
            # if not user_id :
            #     return make_response(jsonify(status=404,msg='user not found.'),404)
            data = getUserMenu(user_id)
        if not data:
           return make_response(jsonify(status=503,msg='Service Unavailable'),503)
           
        return make_response(jsonify(status=200,msg='',data=data),200)