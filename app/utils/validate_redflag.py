
from app.utils.validator import Validator

class Validate_redflag(Validator):

    def __init__(self):
        schema = [
            {'key':'location', 'type':'string', 'not_null':True},
            {'key':'description', 'type':'string', 'not_null':True},
            {'key':'createdOn', 'type':'string', 'not_null':True},
            {'key':'createdby', 'type':'integer', 'not_null':True},
            {'key':'title', 'type':'string', 'not_null':True},
            {'key':'status', 'type':'string', 'not_null':True},
            {'key':'id', 'type':'integer', 'not_null':True},
            {'key':'type', 'type':'string', 'not_null':True}
        ]
        Validator.__init__(self, schema)
