import uuid
from flask import jsonify, Blueprint, request
from project import db
from project.api.api_errors import bad_request, good_request
from project.models import User

api_auth = Blueprint('api_auth', __name__)


@api_auth.route('/api/registration', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'name' not in data or 'password' not in data:
        return bad_request('Must include username and password fields')
    if User.query.filter_by(name=data['name']).first():
        return bad_request('Please use a different username')
    user = User(public_id=str(uuid.uuid4()),)
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    return good_request('Your registration was successful')


@api_auth.route('/api/login', methods=['POST'])
def login_post():
    data = request.get_json() or {}
    name_in_base = User.query.filter_by(name=data['name']).first()
    password_in_base = User.query.filter_by(password=data['password']).first()
    if not name_in_base or not password_in_base:
        return bad_request('Please check your name/password details and try again')
    name_in_base.token = User.get_token(self=name_in_base)
    db.session.commit()
    return jsonify({'token': name_in_base.token})
