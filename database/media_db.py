
from database.connection import cursor

class MediaDB:
    def __init__(self):

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS media (
                id SERIAL PRIMARY KEY,
                type VARCHAR(8) NOT NULL,
                resource TEXT NOT NULL,
                redflag BIGINT NOT NULL REFERENCES redflags(flag_id),
                created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
        )


    def add(self, **kwags):

        medium = f"""INSERT INTO media(type, resource, redflag)\
        VALUES('{kwags["type"]}', '{kwags["input"]}', '{kwags["redflag"]}') RETURNING id;"""

        print(medium)

        try:
            cursor.execute(medium)
            return {'status':True, 'data':cursor.fetchone()}
        except Exception as ex:
            return {'status':False, 'message':format(ex)}

    def update(self, **kwags):
        query = f"""UPDATE media SET resource='{kwags["comment"]}' WHERE id={kwags["id"]} RETURNING id;"""

        print(query)
        try:
            cursor.execute(query)
            return {'status':True, 'data':cursor.fetchone()}
        except Exception as ex:
            return {'status':False, 'message':format(ex)}

    def flag_media(self, **kwags):
        query = f"""SELECT * FROM media WHERE type='{kwags["type"]}' AND redflag='{kwags["redflag"]}';"""
        print(query)
        try:
            cursor.execute(query)
            return {'status':True, 'data':cursor.fetchall()}
        except Exception as ex:
            return {'staus':False, 'message':format(ex)}

    def check_id(self, id):
        query = f"SELECT * FROM media WHERE id='{id}';"
        print(query)

        try:
            cursor.execute(query)
            print("******** in query passed")
            return {'status':True, 'data':cursor.fetchone()}
        except Exception as ex:
            print("******** in query failed")
            return {'status':False, 'message':format(ex)}

    def delete(self, id):
        try:
            cursor.execute(f"delete FROM media where id={id};")
            return {'status':True, 'data':'medium successfully deleted'}
        except Exception as ex:
            return {'status':False, 'message':format(ex)}
