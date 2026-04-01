from flask_swagger_ui import get_swaggerui_blueprint

def init_swagger_ui(app):
    SWAGGER_URL = '/docs'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Portcast API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)