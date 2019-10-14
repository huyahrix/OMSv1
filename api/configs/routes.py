from api.modules.systems.auth import UserLogin
from api.modules.systems.menus import UserMenu

def register_routes(api):
    
    api.add_resource(UserLogin, "/api/v1/system/login")
    api.add_resource(UserMenu,"/api/v1/system/menus")
