
from flask import jsonify
from database.connection import cursor

class UsersDB:
    def __init__(self):

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                userid BIGINT NOT NULL PRIMARY KEY,
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
        try:
            cursor.execute("SELECT * FROM users;")
            return cursor.fetchall()
        except:
            return 'False'

    def update(self, **kwags):
        query = f"""UPDATE users SET firstname='{kwags["firstname"]}', lastname='{kwags["lastname"]}', username='{kwags["username"]}', email='{kwags["email"]}', password='{kwags["password"]}', phonenumber='{kwags["phonenumber"]}', is_admin={kwags["is_admin"]} WHERE userid={kwags["id"]};"""

        print(query)
        try:
            cursor.execute(query)
            return 'True'
        except:
            return 'False'
    
    def check_id(self, id):
        query = f"SELECT * FROM users WHERE userId='{id}';"
        print(query)

        try:
            cursor.execute(query)
            return cursor.fetchone()
        except:
            return 'False'

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
