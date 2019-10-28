from api.modules.systems.auth import Login,Logout,Refresh
from api.modules.systems.menus import Menu
from api.modules.serve.serve import Serve_static, Default

def register_routes(api):

    # Serving static files
    # routes = [
    #     '/<string:filename>',               # webpack file
    #     '/public/images/<string:filename>', # webpack file
    #     '/static/<path:filename>',
    #     ]

    api.add_resource(Default,              '/')
    api.add_resource(Serve_static,         '/static/js/<path:filename>')
    # auth
    api.add_resource(Login,                '/api/v1/system/login')
    api.add_resource(Logout,               '/api/v1/system/logout')
    api.add_resource(Refresh,              '/api/v1/system/refresh')
    api.add_resource(Menu,                 '/api/v1/system/menus')
