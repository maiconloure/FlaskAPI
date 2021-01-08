from flask import Blueprint

bp_status = Blueprint('bp_home', __name__, url_prefix="/status")


@bp_status.route('/')
def status():
    return {'message': 'OK'}
