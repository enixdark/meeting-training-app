from src.api.pool.resources.location_resources import location_routes
from src.api.pool.resources.user_resources import user_routes
from src.api.pool.resources.health_resources import health_routes
from src.api.pool.resources.meeting_resources import meeting_routes


# list mobile routes
mobile_routes = []
mobile_routes.extend(health_routes)
mobile_routes.extend(location_routes)
mobile_routes.extend(user_routes)
mobile_routes.extend(meeting_routes)


# list web routes
web_routes = []
web_routes.extend(health_routes)
web_routes.extend(location_routes)
web_routes.extend(user_routes)
web_routes.extend(meeting_routes)

