from .entities.User import User
from werkzeug.security import generate_password_hash, check_password_hash


class ModelUser():

    @classmethod
    def login(self, conn, username, password):
        print("ENTRO EN MODELUSER.LOGIN")

        try:
            cursor = conn.cursor()

            sql = """
                SELECT id, username, password, fullname, correo, role 
                FROM usuario 
                WHERE username = %s
            """

            cursor.execute(sql, (username,))
            row = cursor.fetchone()

            cursor.close()

            if row is None:
                return None

            # ✅ CORRECCIÓN CLAVE: usar check_password_hash directamente
            if check_password_hash(row[2], password):
                return User(row[0], row[1], row[2], row[3], row[4], row[5])

            return None

        except Exception as ex:
            raise Exception(f"Login error: {ex}")


    @classmethod
    def get_by_id(self, conn, id):
        try:
            cursor = conn.cursor()

            sql = """
                SELECT id, username, password, fullname, correo, role 
                FROM usuario 
                WHERE id = %s
            """

            cursor.execute(sql, (id,))
            row = cursor.fetchone()

            cursor.close()

            if row:
                return User(row[0], row[1], None, row[3], row[4], row[5])

            return None

        except Exception as ex:
            raise Exception(f"Get user error: {ex}")


    @classmethod
    def register(self, conn, user):
        try:
            cursor = conn.cursor()

            password_hash = generate_password_hash(user.password)

            sql = """
                INSERT INTO usuario (username, password, fullname, correo, role)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (
                user.username,
                password_hash,
                user.fullname,
                user.correo,
                user.role
            ))

            conn.commit()
            cursor.close()

        except Exception as ex:
            raise Exception(f"Register error: {ex}")