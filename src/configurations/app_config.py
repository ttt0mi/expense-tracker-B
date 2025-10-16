from datetime import timedelta

from flask import Flask, jsonify
from pydantic import ValidationError
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, ServiceUnavailable

from configurations.database_config import connect_to_mongo
from configurations.extensions import cors, jwt
from configurations.logging_config import get_exp_logger
from configurations.settings import get_settings
from routes.expense_router import expense_bp
from routes.user_router import user_bp

logger = get_exp_logger()


def add_configuration(app: Flask):
	"""jwt keys for the flask-jwt-extended configuration to work.
	you do not need all of them, just the first two"""
	app.config["JWT_SECRET_KEY"] = get_settings().JWT_KEY
	app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
			minutes=get_settings().JWT_ACCESS_TOKEN_EXPIRES)
	app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(
			minutes=get_settings().JWT_REFRESH_TOKEN_EXPIRES
	)
	app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
	app.config["JWT_BLACKLIST_ENABLED"] = True
	app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]


def add_extensions(app: Flask):
	"""to initialise the flask application with flask-cors and flask-jwt-extended instantiated in another module."""
	cors.init_app(app)
	jwt.init_app(app)


def add_blueprints(app: Flask):
	"""to register blueprints to the flask application"""
	app.register_blueprint(user_bp)
	app.register_blueprint(expense_bp)


def add_exception_handlers(app: Flask):
	"""register exception handlers used to the flask application"""
	@app.errorhandler(BadRequest)
	def handle_bad_request(error: BadRequest):
		logger.error(str(error))
		return jsonify({"error": str(error)}), 400

	@app.errorhandler(Unauthorized)
	def handle_unauthorized(error: Unauthorized):
		logger.info(str(error))
		return jsonify({"error": str(error)}), 401

	@app.errorhandler(NotFound)
	def handle_not_found(error: NotFound):
		logger.info(str(error))
		return jsonify({"error": str(error)}), 404

	@app.errorhandler(ServiceUnavailable)
	def handle_service_unavailable(error: ServiceUnavailable):
		logger.critical(str(error))
		return jsonify({"error": str(error)}), 503

	@app.errorhandler(ValidationError)
	def handle_validation_error(error: ValidationError):
		logger.error(error.json(indent=4))
		return jsonify({
				"error": "\n".join([f"{err['msg']}" for err in error.errors()])
		}), 400

	@app.errorhandler(Exception)
	def handle_uncaught_exceptions(error: Exception):
		logger.critical(str(error))
		return jsonify({"error": str(error)}), 500


def create_app(app_name):
	"""app creation factory to avoid filling up the main with unnecessary configurations"""
	connect_to_mongo()
	app = Flask(app_name)
	add_configuration(app)
	add_extensions(app)
	add_blueprints(app)
	add_exception_handlers(app)
	return app