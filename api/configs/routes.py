from api.modules.systems.auth import UserLogin
from api.modules.systems.menus import UserMenu
from api.util.dedault import DefaultRoute

def register_routes(api):
    
    api.add_resource(DefaultRoute,"/")
    api.add_resource(UserLogin, "/api/v1/system/login")
    api.add_resource(UserMenu,"/api/v1/system/menus")
