from .entities.User import User
from werkzeug.security import generate_password_hash, check_password_hash


class ModelUser():

    @classmethod
    def login(self, db, username, password):
        print("ENTRO EN MODELUSER.LOGIN")
        print(username)
        print(password)
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, username, password, fullname,correo, role FROM usuario 
                    WHERE username = '{}'""".format(username)
            cursor.execute(sql)
            row = cursor.fetchone()



            if row is not None:
                if User.check_password(row[2], password):
                    user = User(row[0], row[1], row[2], row[3], row[4], row[5])
                    return user 
                    print(row[5], "ggggggggggg")
                           
               
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, username, password, fullname, correo, role FROM usuario WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[3], row[4], row[5])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def register(self, db, user):
        try:
            cursor = db.connection.cursor()
            print(user.role)

            password_hash = generate_password_hash(user.password)

            sql = """INSERT INTO usuario (username, password, fullname,correo, role)
                     VALUES (%s, %s, %s, %s, %s)"""

            cursor.execute(sql, (user.username, password_hash, user.fullname, user.correo, user.role))
            db.connection.commit()

        except Exception as ex:
            raise Exception(ex)

