from api.modules.systems.auth import UserLogin,UserLogout
from api.modules.systems.menus import UserMenu
from api.util.dedault import DefaultRoute

def register_routes(api):
    
    api.add_resource(DefaultRoute,"/")
    api.add_resource(UserLogin,   "/api/v1/system/login")
    api.add_resource(UserLogout,  "/api/v1/system/logout")
    api.add_resource(UserMenu,    "/api/v1/system/menus")
