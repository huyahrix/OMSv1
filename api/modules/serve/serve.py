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
from flask import current_app, request, jsonify, Response, send_from_directory, make_response, render_template, redirect
from flask_api import status
import os


class Serve_static(Resource):
    def get(self,filename):
        path = current_app.config.get('STATIC_FOLDER')
        if '.js' in filename:
            if current_app.config.get('OS_WIN'):
                path = current_app.config['STATIC_FOLDER'] + '\\js'
            else:
                path = current_app.config['STATIC_FOLDER'] + '/js'
            filename = filename.replace('js/','')
        if '.svg' in filename:
            if current_app.config.get('OS_WIN'):
                path = current_app.config['STATIC_FOLDER'] + '\\images'
            else:
                path = current_app.config['STATIC_FOLDER'] + '/images'
            filename = filename.replace('images/','')

        #if not os.path.exists(path + ('\\','/')[current_app.config.get('OS_WIN')] + filename):
            #return make_response(jsonify(status=404, msg="Cannot find <id={filename}> in {path}".format(filename=filename, path=path)),404)
        return send_from_directory(path,filename)


class Default(Resource):
    def get(self):
        # return redirect("http://www.example.com", code=302)
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'),200,headers)