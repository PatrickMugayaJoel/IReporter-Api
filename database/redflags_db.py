
from database.connection import cursor

class RedflagsDB:

    """ class to handle redflag interactions between application and database """

    def __init__(self):

        """ initializing class. Adding redflags table if not exists """

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS redflags (
                flag_id BIGINT NOT NULL PRIMARY KEY,
                title VARCHAR(30) NOT NULL UNIQUE,
                type VARCHAR(12) NOT NULL,
                status VARCHAR(20) NULL,
                location VARCHAR(20) NOT NULL,
                comment TEXT NULL,
                createdby BIGINT NOT NULL REFERENCES users(userId),
                createdon TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
        )

    
    def regflags(self, type):

        """ function returning redflags from database """

        try:
            reg_flag = f"SELECT * FROM redflags WHERE type = '{type}';"
            cursor.execute(reg_flag)
            print(reg_flag)
            return cursor.fetchall()
        except:
            return 'False'
    
    def register_flag(self, **kwags):

        """ function to add redflags to the database """

        reg_flag = f"""INSERT INTO\
        redflags(flag_id, title, type, status, location, comment, createdby, createdon)\
        VALUES('{kwags["id"]}', '{kwags["title"]}', '{kwags["type"]}', '{kwags["status"]}',\
        '{kwags["location"]}', '{kwags["comment"]}', '{kwags["createdby"]}', '{kwags["createdon"]}');"""

        print(reg_flag)
        try:
            cursor.execute(reg_flag)
            return 'True'
        except:
            return 'False'

    def check_flag(self, id):

        """ function that returns a redflag from database by it's id """

        query = f"SELECT * FROM redflags WHERE flag_id='{id}';"
        print(query)

        try:
            cursor.execute(query)
            return cursor.fetchone()
        except:
            return 'False'

    def check_title(self, title):

        """ selecting a redflag from the database by it's title """

        query = f"SELECT * FROM redflags WHERE title='{title}';"
        print(query)

        try:
            cursor.execute(query)
            return cursor.fetchone()
        except:
            return 'False'

    def delete(self, id):

        """ deleting a redflag from the database """

        query = f"delete FROM redflags WHERE flag_id='{id}';"
        print(query)

        try:
            cursor.execute(query)
            return True
        except:
            return False

    
    def update(self, **kwags):

        """ method to update redflag recode in the database """

        reg_flag = f"""UPDATE redflags SET title='{kwags["title"]}', type='{kwags["type"]}', status='{kwags["status"]}', location='{kwags["location"]}', comment='{kwags["comment"]}' WHERE flag_id={kwags["id"]};"""

        print(reg_flag)
        try:
            cursor.execute(reg_flag)
            return 'True'
        except:
            return 'False'

    def default_flag(self):
        """ method inserting a default flag"""

        try:
            cursor.execute(
                """
                INSERT INTO redflags(flag_id, title, type, status, location, comment, createdby)\
                VALUES(10, 'redflag', 'redflag', 'initial', '0.232, 3.211', 'comment', 10);
                """
            )
            return {"msg":"*** Created default flag ***"}
        
        except Exception as ex:
            return {"defflag":format(ex)}
