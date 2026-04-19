from flask import Flask


def create_app() -> Flask:
	app = Flask(__name__)

	# Register routes after app creation to avoid circular imports.
	from app.routes import register_routes

	register_routes(app)
	return app
