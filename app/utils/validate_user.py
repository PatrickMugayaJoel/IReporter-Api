
from app.utils.validator import Validator

class Validate_user(Validator):

    def __init__(self):
        schema = [
            {'key':'firstname', 'type':'string', 'not_null':True},
            {'key':'lastname', 'type':'string', 'not_null':True},
            {'key':'username', 'type':'string', 'not_null':True},
            {'key':'email', 'type':'email', 'not_null':True},
            {'key':'password', 'type':'string', 'not_null':True},
            {'key':'phonenumber', 'type':'integer', 'not_null':True},
            {'key':'registered', 'type':'string', 'not_null':True},
            {'key':'isAdmin', 'type':'boolean', 'not_null':True},
            {'key':'id', 'type':'integer', 'not_null':True},
            {'key':'othernames', 'type':'string'}
        ]
        Validator.__init__(self, schema)
