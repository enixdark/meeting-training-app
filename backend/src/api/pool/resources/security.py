import datetime
import jwt
import re
from config import BaseApiConfig
from src.api.factory.exceptions.authorized_exceptions import MissingAuthorizationException, \
    InvalidAuthorizationException

__SECRET = BaseApiConfig.SECRET_KEY
__EXP = 7200


def authenticate(user):
    if user is not None:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=__EXP),
            'user': user.serialize()
        }
        encoded = jwt.encode(payload, __SECRET, algorithm='HS256')
        encoded = encoded.decode()
        return encoded
    return None


def identity(authorization) -> dict:
    if authorization:
        try:
            encoded = __get_jwt(authorization)
            decoded = jwt.decode(encoded, __SECRET, algorithms='HS256', options={'verify_exp': False})
            user = decoded.get('user', None)
            return user
        except Exception as e:
            raise InvalidAuthorizationException()
    raise MissingAuthorizationException()


def __get_jwt(authorization):
    pattern = "(?<=^jwt\s).+"
    encoded = re.findall(pattern, authorization)
    return encoded[0]
