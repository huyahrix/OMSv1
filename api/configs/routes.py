from api.modules.systems.auth import Login,Logout,Refresh
from api.modules.systems.menus import Side_navigation_menu, Customize_menu, Bookmarks_menu
from api.modules.serve.serve import Serve_static, Default

def register_routes(api):

    # Serving static files
    # routes = [
    #     '/<string:filename>',               # webpack file
    #     '/public/images/<string:filename>', # webpack file
    #     '/static/<path:filename>',
    #     ]
    
    default = [
        '/',
        '/login'
    ]
    api.add_resource(Default,              *default)
    api.add_resource(Serve_static,         '/static/js/<path:filename>')
    # systems - auth
    api.add_resource(Login,                '/api/v1/system/login')
    api.add_resource(Logout,               '/api/v1/system/logout')
    api.add_resource(Refresh,              '/api/v1/system/refresh')
    # systems - menu
    api.add_resource(Side_navigation_menu, '/api/v1/system/menus')
    api.add_resource(Customize_menu,       '/api/v1/system/menu/customizes')
    api.add_resource(Bookmarks_menu,       '/api/v1/system/menu/bookmarks')
