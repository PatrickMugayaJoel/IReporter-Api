
from flask import jsonify
from database.connection import cursor

class UsersDB:

    """ class to handle user database related activities """

    def __init__(self):

        """ initializing class. creating table users if it does not exist """

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                userid BIGINT NOT NULL PRIMARY KEY,
                username VARCHAR(15) NOT NULL UNIQUE,
                firstname VARCHAR(10) NULL,
                lastname VARCHAR(10) NULL,
                othernames VARCHAR(10) NULL,
                email VARCHAR(20) NOT NULL UNIQUE,
                password VARCHAR(100) NOT NULL,
                is_admin BOOLEAN DEFAULT FALSE,
                phonenumber INTEGER NOT NULL,
                registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
        )


    def register_user(self, **kwags):

        """ function to add a user to the data base """

        reg_user = f"""INSERT INTO\
        users(userid, firstname, lastname, username, email, password, phonenumber, registered)\
        VALUES('{kwags["id"]}', '{kwags["firstname"]}', '{kwags["lastname"]}', '{kwags["username"]}',\
        '{kwags["email"]}', '{kwags["password"]}', '{kwags["phonenumber"]}', '{kwags["registered"]}');"""

        print(reg_user)

        try:
            cursor.execute(reg_user)
            return 'True'
        except:
            return 'False'
    
    def users(self):

        """ function to return users from the database """

        try:
            cursor.execute("SELECT * FROM users;")
            return cursor.fetchall()
        except:
            return 'False'

    def update(self, **kwags):

        """ function to update user data in the database """

        query = f"""UPDATE users SET firstname='{kwags["firstname"]}', lastname='{kwags["lastname"]}', username='{kwags["username"]}', email='{kwags["email"]}', password='{kwags["password"]}', phonenumber='{kwags["phonenumber"]}', is_admin={kwags["is_admin"]} WHERE userid={kwags["id"]};"""

        print(query)
        try:
            cursor.execute(query)
            return 'True'
        except:
            return 'False'
    
    def check_id(self, id):

        """ function to select user from databse by id """

        query = f"SELECT * FROM users WHERE userId='{id}';"
        print(query)

        try:
            cursor.execute(query)
            return cursor.fetchone()
        except:
            return 'False'

    def login(self, username, password):

        """ function to check if the provided username and pasword exist in the database """

        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}';"
        print(query)
        try:
            cursor.execute(query)
            return cursor.fetchone()
        except:
            return 'False'

    def delete_user(self, id):

        """ function to delete a user from the database """

        cursor.execute(f"delete FROM users where userId={id};")

    def delete_default_users(self):

        """ function to clear all database tables (three tables) """

        cursor.execute("delete FROM media;")
        cursor.execute("delete FROM redflags")
        cursor.execute("delete FROM users;")

    def default_users(self):
        """insert a default user"""

        try:
            cursor.execute(
                """
                INSERT INTO users(userid, firstname, lastname, username, email, password, phonenumber, is_admin)\
                VALUES(10, 'admin', 'admin', 'admin', 'admin@admin.go', 'admin', 123456, True ),\
                (20, 'user', 'user', 'user', 'user@user.go', 'user', 123456, False );
                """
            )
            return {"msg":"*** Created default user ***"}
        
        except Exception as ex:
            return {"defusr":format(ex)}
