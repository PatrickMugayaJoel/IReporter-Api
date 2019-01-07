
from flask import jsonify
from database.connection import cursor

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
                password VARCHAR(20) NOT NULL,
                phonenumber INTEGER NOT NULL,
                registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
        )


    def register_user(self, **kwags):

        reg_user = f"""INSERT INTO\
        users(userId, firstname, lastname, username, email, password, phonenumber, registered)\
        VALUES('{kwags["id"]}', '{kwags["firstname"]}', '{kwags["lastname"]}', '{kwags["username"]}',\
        '{kwags["email"]}', '{kwags["password"]}', '{kwags["phonenumber"]}', '{kwags["registered"]}');"""

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
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}';"
        print(query)
        try:
            cursor.execute(query)
            return cursor.fetchone()
        except:
            return 'False'

    def delete_user(self, id):
        cursor.execute(f"delete FROM users where userId={id};")


if __name__ == '__main__':
    db_name = UsersDB()