from flask import Blueprint, request
from http import HTTPStatus
from app.models import Address, db, AddressSchema
from sqlalchemy.exc import IntegrityError
from app.services.address_services import serialize_address, serialize_address_list
from app.services.http import build_api_response

bp_addresses = Blueprint('api_adresses', __name__, url_prefix='/addresses')


@bp_addresses.route('/')
def list_all():
    addresses = Address.query.all()
    address_dicts = serialize_address_list(addresses)

    return {'data': address_dicts}, HTTPStatus.OK


@bp_addresses.route('/', methods=['POST'])
def create():
    data = request.get_json()
    address = Address(
        street=data["street"],
        number=data['number'],
        addr_line1=data['addr_line1'],
        addr_line2=data['addr_line2'],
        postal_code=data['postal_code']
    )

    try:
        db.session.add(address)
        db.session.commit()
        return build_api_response(HTTPStatus.CREATED)
    except IntegrityError:
        return build_api_response(HTTPStatus.BAD_REQUEST)


@bp_addresses.route('/<int:address_id>')
def get(address_id):
    address = Address.query.get(address_id)
    if not address:
        return build_api_response(HTTPStatus.NOT_FOUND)

    return {'data': AddressSchema.dump(address)}


@bp_addresses.route('/<int:address_id>',  methods=['DELETE'])
def delete(address_id):

    if Address.query.filter_by(id=address_id).first() is not None:
        address = Address.query.filter_by(id=address_id).delete()
        db.session.commit()

    else:
        return build_api_response(HTTPStatus.NOT_FOUND)

    return build_api_response(HTTPStatus.OK)
