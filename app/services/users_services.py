from app.services.address_services import serialize_address_list


def serialize_user(user):
    return {
        'id': user.id,
        'name': user.name,
        'surname': user.surname,
        'document': user.document,
        'addresses': serialize_address_list(user.addresses)
    }


def serialize_user_list(user_list):
    return [serialize_user(user) for user in user_list]
