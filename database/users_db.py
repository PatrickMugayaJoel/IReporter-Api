
from flask import jsonify
from database.connection import cursor

class UsersDB:

    """ class to handle user database related activities """

    def __init__(self):

        """ initializing class. creating table users if it does not exist """

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                userid SERIAL PRIMARY KEY,
                username VARCHAR(25) NOT NULL UNIQUE,
                firstname VARCHAR(25) NULL,
                lastname VARCHAR(25) NULL,
                othernames VARCHAR(25) NULL,
                email VARCHAR(30) NOT NULL UNIQUE,
                password VARCHAR(25) NOT NULL,
                is_admin BOOLEAN DEFAULT FALSE,
                phonenumber INTEGER NOT NULL,
                registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
        )


    def register_user(self, **kwags):

        """ function to add a user to the data base """

        reg_user = f"""INSERT INTO users(firstname, lastname, username, email, password, phonenumber, registered)
                        VALUES('{kwags["firstname"]}', '{kwags["lastname"]}', '{kwags["username"]}', '{kwags["email"]}', '{kwags["password"]}', '{kwags["phonenumber"]}', '{kwags["registered"]}') RETURNING userid;"""

        try:
            cursor.execute(reg_user)
            reg_user=cursor.fetchone()
            return {'status':True, 'data':reg_user}
        except Exception as e:
            return {'status':False, 'error':str(e)}
    
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

        try:
            cursor.execute(query)
            return 'True'
        except:
            return 'False'
    
    def check_id(self, id):

        """ function to select user from databse by id """

        query = f"SELECT * FROM users WHERE userId='{id}';"

        try:
            cursor.execute(query)
            return cursor.fetchone()
        except:
            return 'False'

    def login(self, username, password):

        """ function to check if the provided username and pasword exist in the database """

        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}';"
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

        cursor.execute("drop table if exists media;")
        cursor.execute("drop table if exists incidents")
        cursor.execute("drop table if exists users;")

    def default_users(self):
        """insert a default user"""

        try:
            cursor.execute(
                """
                INSERT INTO users(firstname, lastname, username, email, password, phonenumber, is_admin)\
                VALUES('admin', 'admin', 'admin', 'admin@admin.go', 'admin', 123456, True ),\
                ('user', 'user', 'user', 'user@user.go', 'user', 123456, False );
                """
            )
            return {"msg":"*** Created default user ***"}
        
        except Exception as ex:
            return {"defusr":format(ex)}
