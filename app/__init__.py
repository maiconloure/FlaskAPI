from flask import Flask, render_template
from app.views.status import bp_status
from app.views.users import bp_users
from app.views.address import bp_addresses
from app.models import db, mg, ma
from environs import Env


def create_app():
    env = Env()
    env.read_env()

    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = env.bool(
        'SQLALCHEMY_TRACK_MODIFICATIONS')
    app.config['SQLALCHEMY_DATABASE_URI'] = env.str('SQLALCHEMY_DATABASE_URI')

    db.init_app(app)
    mg.init_app(app, db)
    ma.init_app(app)

    @app.route('/')
    def homepage():
        return render_template("index.html", title="HOME PAGE")

    app.register_blueprint(bp_status)
    app.register_blueprint(bp_users)
    app.register_blueprint(bp_addresses)

    return app
