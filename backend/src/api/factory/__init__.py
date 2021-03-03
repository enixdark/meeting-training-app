from flask import Flask, g
from flask_cors import CORS


class Factory:

    def __init__(self, app_name, config, routes, db):
        self.app_name = app_name
        self.config = config
        self.routes = routes
        self.db = db

    def create_app(self):
        app = Flask(__name__)
        CORS(app=app, supports_credentials=True,
             automatic_options=True)

        @app.before_request
        def before_request():
            g.session = self.db.get_session()

        @app.after_request
        def after_request(response):
            g.session.close()
            return response

        app.config.from_object(self.config)
        self.__init_routes(app, self.routes)

        return app

    @staticmethod
    def __init_routes(app, routes: list):
        for route in routes:
            uri = route.get('uri', None)
            view_func = route.get('view', None)
            methods = route.get('methods', None)
            if uri and view_func and methods:
                app.add_url_rule('/{}'.format(uri), view_func=view_func, methods=methods)
