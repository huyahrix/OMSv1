from api.modules.systems.auth import UserLogin
from api.modules.systems.menus import UserMenu

def register_routes(api):
    
    from api.util.dedault_route import DefaultRoute
    api.add_resource(UserLogin, "/api/v1/system/login")
    api.add_resource(UserMenu,"/api/v1/system/menus")
    api.add_resource(DefaultRoute,"/")
