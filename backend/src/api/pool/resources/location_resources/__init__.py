from .location_list_resource import ListLocationAPI
from .location_resource import LocationAPI
from .location_xls_resource import LocationXLSAPI

location_view = LocationAPI.as_view('location_api')
list_location_view = ListLocationAPI.as_view('list_location_api')
xls_view = LocationXLSAPI.as_view('xls_api')

location_routes = [
    {
        'uri': 'location/get',
        'view': location_view,
        'methods': ['GET', ]
    },
    {
        'uri': 'location/post',
        'view': location_view,
        'methods': ['POST', ]
    },
    {
        'uri': 'location/patch',
        'view': location_view,
        'methods': ['PATCH', ]
    },
    {
        'uri': 'location/delete',
        'view': location_view,
        'methods': ['DELETE', ]
    },
    {
        'uri': 'location/all',
        'view': list_location_view,
        'methods': ['GET', ]
    },
    {
        'uri': 'location/export',
        'view': xls_view,
        'methods': ['POST', ]
    },
]
