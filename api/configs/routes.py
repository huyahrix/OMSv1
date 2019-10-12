from api.modules.systems.auth import UserLogin
from api.modules.systems.menus import Menu

def register_routes(api):
    
    api.add_resource(UserLogin, "/api/v1/system/login")
    api.add_resource(Menu,"/api/v1/system/menus")
