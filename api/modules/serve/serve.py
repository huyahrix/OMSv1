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
from flask import current_app, request, jsonify, Response, send_from_directory, make_response, render_template
from flask_api import status
import os


class Serve_static(Resource):
    #@jwt_required
    def get(self,filename):
        current_app.logger.debug('serve : %f',filename) 
        path = current_app.config['STATIC_FOLDER']
        if 'js/' in filename:
            if current_app.config.get('OS_WIN'):
                path = current_app.config['STATIC_FOLDER'] + '\\js'
            else:
                path = current_app.config['STATIC_FOLDER'] + '/js'
            filename = filename.replace('js/','')
        print(filename)
        if not os.path.exists(path + '\\' + filename):
            return make_response(jsonify(status=status.HTTP_200_OK, msg="Cannot find <id={filename}> in {path}".format(filename=filename, path=path)),404)
        return send_from_directory(path,filename)

        # STATIC_FOLDER = 'd:\\Privite\\Python\\OMSv1\\api\\static'
        # path = current_app.config['STATIC_FOLDER'] + filename
        # #return send_from_directory(current_app.config['STATIC_FOLDER'], 'index.html')
        # return send_from_directory('d:\\Privite\\Python\\OMSv1\\api\\static\\js','runtime.912487c9b6fba62d63dc.js')


class Default(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        # if not os.path.exists(path + '\\' + filename):
        #     return make_response(jsonify(status=status.HTTP_200_OK, msg="Cannot find <id={filename}> in {path}".format(filename=filename, path=path)),404)
        return make_response(render_template('index.html'),200,headers)


class Render(Resource):
    def get(self):
         message = "Hello, World"
         headers = {'Content-Type': 'text/html'}
         path = current_app.config['TEMPLATES_FOLDER'] + '\\render.html'
         return make_response(render_template('render.html',message=message),200,headers)
         #return render_template('index.html',message=message)
