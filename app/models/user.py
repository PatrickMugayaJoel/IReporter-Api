
class User:

    """ User model structure """

    def __init__(self, **kwags):
    
        self.firstname = kwags.get('firstname')
        self.lastname = kwags.get('lastname')
        self.username = kwags.get('username')
        self.email = kwags.get('email')
        self.password = kwags.get('password')
        self.phonenumber = kwags.get('phonenumber')
        self.registered = kwags.get('registered')
        self.isAdmin = kwags.get('isAdmin')
        self.id = kwags.get('id')
        self.othernames = kwags.get('othernames')
