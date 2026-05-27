from flask import Flask, render_template, session
from config import Config
from database import Database
from routes import main_bp, auth_bp, cart_bp, api_bp, admin_bp


def create_app() -> Flask:
    app = Flask(__name__, instance_path=Config.INSTANCE_PATH)
    app.secret_key = Config.SECRET_KEY

    db = Database(Config.DB_PATH)
    db.init_schema()
    app.config['db'] = db

    for bp in (main_bp, auth_bp, cart_bp, api_bp, admin_bp):
        app.register_blueprint(bp)

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    @app.context_processor
    def inject_globals():
        cart = session.get('cart', [])
        return {'cart_count': sum(c['qty'] for c in cart)}

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
