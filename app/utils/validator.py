
import re

class Validator:
    """ Data validation methods """

    def __init__(self, schema):
        """ class variables """

        self.__invalid_data_messages = list()
        self.__schema = schema
    
    def validate(self, **kwargs):
        """ setting data and calling validating methods """

        self.data = kwargs
        self.__worker()

        if self.__invalid_data_messages:
            return({'status':False, 'message':self.__invalid_data_messages})
        else:
            return({'status':True, 'message':'successfully validated'})

        self.__invalid_data_messages.clear()

    def __worker(self):
        """ Seperating data types """

        dispatch = {
            'string':self.__valid_string,
            'integer':self.__is_valid_integer,
            'email':self.__is_valid_email
        }

        for item in self.__schema:
            """ loop through a schemma assigning a function to do the actual check """

            item = self.__add_value_to_item(item)
            
            func = dispatch.get(item.get('type'), lambda a: "Invalid type")
            func(item)

            if item.get('not_null') == True:
                self.__is_not_null(item)

            if isinstance(item.get('min_length'), int):
                self.__is_min_length(item)

    def __add_value_to_item(self, item):
        """ adding user input to a schema item """

        if (self.data.get(item['key']) == False) or self.data.get(item['key']):
            item.update(value = self.data[item['key']])
        elif item.get('not_null') == True:
            self.__invalid_data_messages.append(item['key']+" can not be empty.")
            item={}
        else:
            item={}
        
        return item

    def __valid_string(self, mystring):
        """ function that validates a string """

        if not isinstance(mystring['value'], str) or mystring['value'].isspace():
            self.__invalid_data_messages.append(mystring['key']+" must be a string.")

    def __is_valid_email(self, item):
        """ Validating email """

        if isinstance(item['value'], str):
            if re.match(r"[^@.]+@[A-Za-z]+\.[a-z]+", item['value']) == None:
                self.__invalid_data_messages.append(item['key']+" is invalid.")
        else:
            self.__invalid_data_messages.append(item['key']+" must be a string.")

    def __is_valid_integer(self, myinteger):
        """ Validate if is an integer """

        if not (isinstance(myinteger['value'], int)):
            self.__invalid_data_messages.append(f"{myinteger['key']} must be an integer.")

    def __is_min_length(self, item):
        """ Validating if is correct min length """

        item['value'] = str(item['value'])

        if not len(item['value'])>(item['min_length']-1):
            self.__invalid_data_messages.append(item['key']+" must be at least "+str(item['min_length'])+" characters long.")

    def __is_not_null(self, item):
        """ Validating if not null """

        if not isinstance(item['value'], str):
            item['value'] = str(item['value'])

        if not len(item['value'])>0:
            self.__invalid_data_messages.append(item['key']+" can not be empty.")
