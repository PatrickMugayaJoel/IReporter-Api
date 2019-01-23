
from database.connection import cursor
from database.connection import curs

class MediaDB:

    """ class to handle database application interactions for images and videos """

    def __init__(self):

        """ initalizing the class. creating a table media if it does not exist """

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

        """ method to save videos/images to the database """

        medium = f"""INSERT INTO media(type, resource, redflag)\
        VALUES('{kwags["type"]}', '{kwags["input"]}', '{kwags["redflag"]}') RETURNING id;"""

        print(medium)

        try:
            cursor.execute(medium)
            return {'status':True, 'data':cursor.fetchone()}
        except Exception as ex:
            return {'status':False, 'message':format(ex)}

    def update(self, **kwags):

        """ method to update data in the media table """

        query = f"""UPDATE media SET resource='{kwags["comment"]}' WHERE id={kwags["id"]} RETURNING id;"""
        print(query)
        try:
            cursor.execute(query)
            return {'status':True, 'data':cursor.fetchone()}
        except Exception as ex:
            return {'status':False, 'message':format(ex)}

    def flag_media(self, **kwags):

        """ method to select data from media table """

        query = f"""SELECT resource FROM media WHERE type='{kwags["type"]}' AND redflag='{kwags["redflag"]}';"""
        print(query)
        try:
            curs.execute(query)
            result = curs.fetchall()
            return {'status':True, 'data':result}
        except Exception as ex:
            return {'staus':False, 'message':format(ex)}

    def check_id(self, id):

        """ method to select data from media table by id """

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

        """ method to delete image/video from """

        try:
            cursor.execute(f"delete FROM media where id={id};")
            return {'status':True, 'data':'medium successfully deleted'}
        except Exception as ex:
            return {'status':False, 'message':format(ex)}
