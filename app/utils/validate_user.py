
from app.utils.validator import Validator


class Validate_user(Validator):

    """ inherits the validator """

    def __init__(self):
        """ Method declares the schemma aganist which a user is to be validated """

        schema = [
            {'key': 'firstname', 'type': 'string',
                'not_null': True, 'max_length': 25},
            {'key': 'lastname', 'type': 'string',
                'not_null': True, 'max_length': 25},
            {'key': 'username', 'type': 'string',
                'not_null': True, 'max_length': 25},
            {'key': 'email', 'type': 'email', 'not_null': True, 'max_length': 30},
            {'key': 'password', 'type': 'string',
                'not_null': True, 'max_length': 25},
            {'key': 'phonenumber', 'type': 'integer',
                'not_null': True, 'max_length': 16},
            {'key': 'registered', 'type': 'string', 'not_null': True},
            {'key': 'is_admin', 'type': 'boolean', 'not_null': True},
            {'key': 'othernames', 'type': 'string', 'max_length': 25}
        ]
        Validator.__init__(self, schema)
