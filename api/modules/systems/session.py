#  @copyright 2019 © DigiNet
#  @author ahrix<infjnite@gmail.com>
#  @create 2019/10/29 09:04
#  @update 2019/10/29 09:04

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
from api.resources.system import getUserMenu, getCustomizeMenu, GetBookmarkMenu