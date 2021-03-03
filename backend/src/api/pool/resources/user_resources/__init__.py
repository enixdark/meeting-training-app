from .code_user_resource import CodeUserAPI
from .suggest_user_resource import SuggestUserAPI
from .token_user_resource import TokenUserAPI
from .user_auth_resource.user_confirm_resource import UserConfirmAuthAPI

from .user_auth_resource import auth_user_routes

user_view = TokenUserAPI.as_view('user_api')
code_user_view = CodeUserAPI.as_view('code_user_api')
suggest_user_view = SuggestUserAPI.as_view('suggest_user_api')
confirm_view = UserConfirmAuthAPI.as_view('confirm_api')

user_prefix = 'user'

user_routes = [
    {
        'uri': 'login',
        'view': user_view,
        'methods': ['POST', ]
    },
    {
        'uri': 'login_code',
        'view': code_user_view,
        'methods': ['POST', ]
    },
    {
        'uri': 'user/suggest',
        'view': suggest_user_view,
        'methods': ['GET', ]
    },
]

user_routes.extend(auth_user_routes)
