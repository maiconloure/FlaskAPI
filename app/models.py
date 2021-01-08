from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy.fields import Nested

db = SQLAlchemy()
mg = Migrate()
ma = Marshmallow()

user_address = db.Table(
    'user_address',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('address_id', db.Integer, db.ForeignKey('address.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    surname = db.Column(db.String, unique=False, nullable=True)
    document = db.Column(db.String(1024), unique=True, nullable=False)

    accounts = db.relationship("CCAccount", back_populates="user")

    addresses = db.relationship(
        "Address", secondary=user_address, back_populates="users")

    def __repr__(self):
        return f'<User name={self.name} document={self.document}'


class CCAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agency = db.Column(db.String, nullable=False)
    number = db.Column(db.String, nullable=False)
    money = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship("User", back_populates="accounts")


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=True)
    addr_line1 = db.Column(db.String, nullable=True)
    addr_line2 = db.Column(db.String, nullable=True)
    postal_code = db.Column(db.String, nullable=False)

    users = db.relationship(
        "User", secondary=user_address, back_populates="addresses")


class AddressSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Address

    id = ma.auto_field()
    street = ma.auto_field()
    number = ma.auto_field()
    addr_line1 = ma.auto_field()
    addr_line2 = ma.auto_field()
    postal_code = ma.auto_field()


class UserSchema(ma.SQLAlchemySchema):

    class Meta:
        model = User

    id = ma.auto_field()
    name = ma.auto_field()
    surname = ma.auto_field()
    document = ma.auto_field()
    addresses = ma.auto_field()

    addresses = Nested(AddressSchema, many=True)
