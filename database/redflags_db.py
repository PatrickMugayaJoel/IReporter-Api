
from database.connection import cursor

class RedflagsDB:
    def __init__(self):

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS redflags (
                flag_id BIGINT NOT NULL PRIMARY KEY,
                title VARCHAR(20) NOT NULL UNIQUE,
                type VARCHAR(8) NOT NULL,
                status VARCHAR(20) NULL,
                location VARCHAR(20) NOT NULL,
                description TEXT NULL,
                createdBy BIGINT NOT NULL REFERENCES users(userId),
                createdOn TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
        )

    
    def regflags(self):
        try:
            cursor.execute("SELECT * FROM redflags;")
            return cursor.fetchall()
        except:
            return 'False'
    
    def register_flag(self, **kwags):
        reg_flag = f"""INSERT INTO\
        redflags(flag_id, title, type, status, location, description, createdBy, createdOn)\
        VALUES('{kwags["id"]}', '{kwags["title"]}', '{kwags["type"]}', '{kwags["status"]}',\
        '{kwags["location"]}', '{kwags["description"]}', '{kwags["createdBy"]}', '{kwags["createdOn"]}');"""

        print(reg_flag)
        try:
            cursor.execute(reg_flag)
            return 'True'
        except:
            return 'False'

    def check_flag(self, id):
        query = f"SELECT * FROM redflags WHERE flag_id='{id}';"
        print(query)

        try:
            cursor.execute(query)
            return cursor.fetchone()
        except:
            return 'False'
    
    def check_title(self, title):
        query = f"SELECT * FROM redflags WHERE title='{title}';"
        print(query)

        try:
            cursor.execute(query)
            return cursor.fetchone()
        except:
            return 'False'

    def delete(self, id):
        query = f"delete FROM redflags WHERE flag_id='{id}';"
        print(query)

        try:
            cursor.execute(query)
            return True
        except:
            return False

    
    def update(self, **kwags):
        reg_flag = f"""UPDATE redflags SET title='{kwags["title"]}', type='{kwags["type"]}', status='{kwags["status"]}', location='{kwags["location"]}', description='{kwags["description"]}' WHERE flag_id={kwags["id"]};"""

        print(reg_flag)
        try:
            cursor.execute(reg_flag)
            return 'True'
        except:
            return 'False'


if __name__ == '__main__':
    db_name = RedflagsDB()
