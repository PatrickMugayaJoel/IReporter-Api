
from app.utils.validator import Validator

class Validate_redflag(Validator):

    """ class inherits from validator """

    def __init__(self):
            
        """ Method declares the schemma aganist which a redflag is to be validated """

        schema = [
            {'key':'location', 'type':'string', 'not_null':True},
            {'key':'comment', 'type':'string', 'not_null':True},
            {'key':'createdon', 'type':'string', 'not_null':True},
            {'key':'createdby', 'type':'integer', 'not_null':True},
            {'key':'title', 'type':'string', 'not_null':True},
            {'key':'status', 'type':'string', 'not_null':True},
            {'key':'id', 'type':'integer', 'not_null':True}
        ]
        Validator.__init__(self, schema)
