
from database.connection import cursor

class IncidentsDB:

    """ class to handle redflag interactions between application and database """

    def __init__(self):

        """ initializing class. Adding incidents table if not exists """

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS incidents (
                flag_id SERIAL PRIMARY KEY,
                title VARCHAR(50) NOT NULL UNIQUE,
                type VARCHAR(12) NOT NULL,
                status VARCHAR(20) NULL,
                location VARCHAR(40) NOT NULL,
                comment TEXT NULL,
                username VARCHAR(25),
                createdby BIGINT NOT NULL REFERENCES users(userId),
                createdon TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
        )

    
    def regflags(self, type):

        """ function returning incidents from database """

        try:
            reg_flag = f"SELECT * FROM incidents;"
            cursor.execute(reg_flag)
            return cursor.fetchall()
        except:
            return 'False'
    
    def regflagsbyuser(self, userid):

        """ function returning incidents from database """

        try:
            reg_flag = f"SELECT * FROM incidents WHERE createdby = '{userid}';"
            cursor.execute(reg_flag)
            return cursor.fetchall()
        except:
            return 'False'

    def register_flag(self, **kwags):

        """ function to add incidents to the database """

        reg_flag = f"""INSERT INTO\
        incidents(title, type, status, location, comment, createdby, username, createdon)\
        VALUES('{kwags["title"]}', '{kwags["type"]}', '{kwags["status"]}',\
        '{kwags["location"]}', '{kwags["comment"]}', '{kwags["createdby"]}', '{kwags["username"]}', '{kwags["createdon"]}') RETURNING flag_id;"""

        try:
            cursor.execute(reg_flag)
            flag=cursor.fetchone()
            return {'status':True, 'data':flag}
        except Exception as e:
            return {'status':False, 'error':str(e)}

    def check_flag(self, id):

        """ function that returns a redflag from database by it's id """

        query = f"SELECT * FROM incidents WHERE flag_id='{id}';"

        try:
            cursor.execute(query)
            return cursor.fetchone()
        except:
            return 'False'

    def check_title(self, title):

        """ selecting a redflag from the database by it's title """

        query = f"SELECT * FROM incidents WHERE title='{title}';"

        try:
            cursor.execute(query)
            return cursor.fetchone()
        except:
            return 'False'

    def delete(self, id):

        """ deleting a redflag from the database """

        query = f"delete FROM incidents WHERE flag_id='{id}';"

        try:
            cursor.execute(query)
            return True
        except:
            return False

    
    def update(self, **kwags):

        """ method to update redflag recode in the database """

        reg_flag = f"""UPDATE incidents SET title='{kwags["title"]}', type='{kwags["type"]}', status='{kwags["status"]}', location='{kwags["location"]}', comment='{kwags["comment"]}' WHERE flag_id={kwags["id"]};"""

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
                INSERT INTO incidents(title, type, status, location, comment, createdby, username)\
                VALUES('redflag', 'redflag', 'initial', '0.232, 3.211', 'comment', 1, 'admin');
                """
            )
            return {"msg":"*** Created default flag ***"}
        
        except Exception as ex:
            return {"defflag":format(ex)}
