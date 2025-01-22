from flask import Flask

from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SECRET_KEY'] = 'AIzaSyCZyIERF87OzHD_QbrkiYgXs68jjVZN7dQ'

    # Initialize Flask extensions here

    # Register Blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    @app.route('/test')
    def test_page():
        return '<h1>Testing the page</h1>'
    
    return app