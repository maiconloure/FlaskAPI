from flask import Blueprint, request
from app.models import User, Address, UserSchema
from app.models import db
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from app.services.http import build_api_response
from app.services.users_services import serialize_user, serialize_user_list
bp_users = Blueprint('api_users', __name__, url_prefix="/users")


@bp_users.route('/')
def list_all():
    users = User.query.all()
    user_dicts = serialize_user_list(users)

    return {'data': user_dicts}, HTTPStatus.OK


@bp_users.route('/', methods=['POST'])
def create():
    user_data = request.get_json()
    user = User(
        name=user_data["name"],
        surname=user_data['surname'],
        document=user_data['document']
    )

    try:
        db.session.add(user)
        db.session.commit()
        return build_api_response(HTTPStatus.CREATED)

    except IntegrityError:
        return build_api_response(HTTPStatus.BAD_REQUEST)


@bp_users.route('/<int:user_id>')
def get(user_id):
    user = User.query.get(user_id)
    if not user:
        return build_api_response(HTTPStatus.NOT_FOUND)

    return {'data': UserSchema().dump(user)}


@bp_users.route('/<int:user_id>', methods=['PUT'])
def put(user_id):
    data = request.get_json()
    user = User.query.get(user_id)

    user.document = data['document'] if data.get('document') else user.document
    user.name = data['name'] if data.get('name') else user.name
    user.surname = data['surname'] if data.get('surname') else user.surname

    addresses = Address.query.filter(Address.id.in_(data['addresses']))
    for address in addresses:
        user.addresses.append(address)

    db.session.commit()

    if not user:
        return build_api_response(HTTPStatus.NOT_FOUND)

    return serialize_user(user)
