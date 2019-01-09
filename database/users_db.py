
from flask import jsonify
from database.connection import cursor
from werkzeug.security import generate_password_hash

class UsersDB:
    def __init__(self):

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                userId BIGINT NOT NULL PRIMARY KEY,
                username VARCHAR(15) NOT NULL UNIQUE,
                firstname VARCHAR(10) NULL,
                lastname VARCHAR(10) NULL,
                email VARCHAR(20) NOT NULL UNIQUE,
                password VARCHAR(100) NOT NULL,
                is_admin BOOLEAN DEFAULT FALSE,
                phonenumber INTEGER NOT NULL,
                registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tokens (
            id SERIAL PRIMARY KEY,token TEXT,
            is_valid BOOLEAN DEFAULT TRUE,
            last_used TIMESTAMPTZ DEFAULT Now());
            """
        )


    def register_user(self, **kwags):

        password = generate_password_hash(kwags["password"])

        reg_user = f"""INSERT INTO\
        users(userId, firstname, lastname, username, email, password, phonenumber, registered)\
        VALUES('{kwags["id"]}', '{kwags["firstname"]}', '{kwags["lastname"]}', '{kwags["username"]}',\
        '{kwags["email"]}', '{password}', '{kwags["phonenumber"]}', '{kwags["registered"]}');"""

        print(reg_user)

        try:
            cursor.execute(reg_user)
            return 'True'
        except:
            return 'False'
    
    def users(self):
        try:
            cursor.execute("SELECT * FROM users;")
            return cursor.fetchall()
        except:
            return 'False'
    
    def check_username(self, username):
        query = f"SELECT * FROM users WHERE username='{username}';"
        print(query)

        try:
            cursor.execute(query)
            return cursor.fetchone()
        except:
            return False

    def check_email(self, email):
        query = f"SELECT * FROM users WHERE email='{email}';"
        print(query)

        try:
            cursor.execute(query)
            return cursor.fetchone()
        except:
            return False
    
    def check_id(self, id):
        query = f"SELECT * FROM users WHERE userId='{id}';"
        print(query)

        try:
            cursor.execute(query)
            return cursor.fetchone()
        except:
            return False

    def login(self, username, password):
        password = generate_password_hash(password)
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}';"
        print(query)
        try:
            cursor.execute(query)
            return cursor.fetchone()
        except:
            return 'False'

    def delete_user(self, id):
        cursor.execute(f"delete FROM users where userId={id};")



    def save_token(self, token):
        query = f"INSERT INTO tokens(token) VALUES('{token}')"
        cursor.execute(query)

    def invalidate_a_token(self, token):
        query = "UPDATE tokens SET is_valid  ={} WHERE token = '{}'".format(False, token)
        cursor.execute(query)

    def is_token_invalid(self, token):
        query = "SELECT is_valid FROM tokens WHERE token={}".format(token)
        cursor.execute(query)
        
        results = cursor.fetchone()
        return results[0]


if __name__ == '__main__':
    db_name = UsersDB()
