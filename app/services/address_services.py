def serialize_address(address):
    return {
        'id': address.id,
        'number': address.number,
        'addr_line1': address.addr_line1,
        'addr_line2': address.addr_line2,
        'postal_code': address.postal_code
    }


def serialize_address_list(address_list):
    return [serialize_address(address) for address in address_list]
