from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt

from configurations.dependencies import get_user_handler
from configurations.extensions import jwt
from schemas.user_schemas import CreateUser, LoginRequest, UpdateUser

user_bp = Blueprint('user routes', __name__, url_prefix='/user')


@user_bp.route('/register', methods=['POST'])
def user_registration():
	user_handler = get_user_handler()
	user_data = request.get_json()
	new_user = CreateUser(**user_data)
	registered_user_data = user_handler.register_user(new_user)
	return jsonify({
				"user_id": registered_user_data["id"],
				"email": registered_user_data["email"]}
	), 201


@user_bp.route('/login', methods=['POST'])
def user_login():
	user_handler = get_user_handler()
	login_request = LoginRequest(
			email=request.form.get("email"),
			password=request.form.get("password")
	)
	user_data = user_handler.verify_user(login_request)
	token = create_access_token(identity=user_data["id"])
	return jsonify(access_token=token), 200


@user_bp.route('/update', methods=['PATCH'])
@jwt_required()
def user_update():
	logged_in_user_id = get_jwt_identity()
	user_handler = get_user_handler()
	update_data = request.get_json()
	update_user = UpdateUser(id=logged_in_user_id, **update_data)
	user_data = user_handler.update_user(update_user)
	return jsonify(user_data), 200


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
	user_handler = get_user_handler()
	jti = jwt_payload["jti"]
	return user_handler.is_token_blacklisted(jti)


@user_bp.route('/logout', methods=['POST'])
@jwt_required()
def user_logout():
	user_handler = get_user_handler()
	jti = get_jwt().get("jti")
	user_handler.blacklist_token(jti)
	return jsonify({
			"success": True,
			"message": "User logout successfully"
	}), 200