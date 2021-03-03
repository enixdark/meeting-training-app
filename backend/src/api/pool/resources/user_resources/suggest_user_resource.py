from src.api.pool.decorators.user_decorators.suggest_decorator import UserSuggestDecorator
from src.api.pool.resources.entities.responses.implement_responses.method_responses.get_responses.user_get_responses import \
    UserSuggestNoneResourceResponse, UserSuggestResourceResponse
from .. import Resource, Service, Request, BaseAPI
from ..entities.requests.implement_requests.user_requests.user_suggest_request import UserSuggestRequest


class SuggestUserResource(Resource):
    def _create_service(self) -> Service:
        return UserSuggestDecorator()

    def get(self, request: Request, *args, **kwargs):
        suggest_users = self._service.get_all(**request.all())
        if len(suggest_users) == 0:
            self._set_response(UserSuggestNoneResourceResponse())
            return []
        self._set_response(UserSuggestResourceResponse())
        relations = request.get('relations')
        return [user.serialize(inclusion_rs=relations) for user in suggest_users]


class SuggestUserAPI(BaseAPI):
    def _create_resource(self) -> Resource:
        return SuggestUserResource()

    GET = {
        'request': UserSuggestRequest
    }
