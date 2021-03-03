from .health_resouce import HealthAPI

health_view = HealthAPI.as_view('health_api')

health_routes = [
    {
        'uri': 'healthcheck',
        'view': health_view,
        'methods': ['GET', ]
    },
]
