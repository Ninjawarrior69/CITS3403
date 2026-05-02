from flask import Flask

from app.config import Config
from app.extensions import csrf, db, login_manager, migrate


def create_app() -> Flask:
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	migrate.init_app(app, db)
	login_manager.init_app(app)
	login_manager.login_view = "login"
	csrf.init_app(app)

	# Import models so Flask-Migrate can detect schema metadata.
	from app import models  # noqa: F401

	# Register user loader for Flask-Login
	@login_manager.user_loader
	def load_user(user_id):
		return models.User.query.get(int(user_id))

	# Register routes after app creation to avoid circular imports.
	from app.routes import register_routes

	register_routes(app)
	return app
