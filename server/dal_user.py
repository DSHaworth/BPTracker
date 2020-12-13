from contextlib import closing
from db_core import DB_core
from models import User

class DAL_user:

    @classmethod
    def add_user(cls, user):
        con = DB_core.connect()
        with closing(con.cursor()) as c:
            c.execute("""
                INSERT INTO users 
                    (email, password, firstname, lastname, dob, image)
                VALUES
                    (?, ?, ?, ?, ?, ?)""", (user.email, user.password, user.firstname, user.lastname, user.dob, user.image,))
            con.commit()
        return user

    @classmethod
    def get_all_users(cls):
        con = DB_core.connect()
        with closing(con.cursor()) as c:
            c.execute("""
                SELECT 
                    userId, email, firstname, lastname, image
                FROM
                    users""")
            rows = c.fetchall()

        users = []
        for row in rows:
            users.append(User(userId=row["userId"], email=row["email"], firstname=row["firstname"], lastname=row["lastname"], image=row["image"]).to_dict())
        return users        

    @classmethod
    def get_user_by_id(cls, id):
        con = DB_core.connect()
        with closing(con.cursor()) as c:
            c.execute("""
                SELECT 
                    userId, email, firstname, lastname, image
                FROM
                    users
                WHERE
                    userId=?""", (id,))
            row = c.fetchone()

        if row:
            return User(userId=row["userId"], email=row["email"], firstname=row["firstname"], lastname=row["lastname"], image=row["image"]).to_dict()
        else:
            return None

    @classmethod
    def validate_user(cls, userId, email, password):

        con = DB_core.connect()
        with closing(con.cursor()) as c:
            c.execute("""
                SELECT 
                    userId, email, password
                FROM
                    users
                WHERE
                    userId=?
                AND
                    email=?""", (userId, email,))
            row = c.fetchone()

        if row:
            if User.authenticate(row["password"], password):
                return cls.get_user_by_id(row["userId"])
            else:
                return None
        else:
            return None

    @classmethod
    def update_user(cls, user):
        con = DB_core.connect()
        with closing(con.cursor()) as c:
            c.execute("""
        UPDATE users 
            SET 
                email = ?, 
                firstname = ?, 
                lastname = ?, 
                dob = ?, 
                image = ?
            WHERE 
                userId = ?""", (user.email, user.firstname, user.lastname, user.dob, user.image, user.userId))
            con.commit()
        return user

    @classmethod
    def update_user_password(cls, user):
        con = DB_core.connect()
        with closing(con.cursor()) as c:
            c.execute("""
        UPDATE users 
            SET 
                password = ?            
            WHERE 
                userId = ?""", (user.password, user.userId))
            con.commit()
        return user

    @classmethod
    def make_user(cls, row):
        return User(userId=row["userId"], email=row["email"], firstname=row["firstname"], lastname=row["lastname"], dob=row["dob"], image=row["image"])

    ##### TESTS START ############
    @classmethod
    def add_user_test(cls):
        """
        userId, email, password, firstname, lastname, dob, image
        """
        email=input("email: ")
        password=input("password: ")
        firstname=input("firstname: ")
        lastname=input("lastname: ")
        dob=input("dob: ")

        user = cls.add_user(User(email=email, password=password, firstname=firstname, lastname=lastname, dob=dob))
        print(user)

    @classmethod
    def get_all_users_test(cls):
        users = cls.get_all_users()
        for user in users:
            print(user.__dict__)

    @classmethod
    def get_user_by_id_test(cls):
        id = int(input("Id to fetch: "))
        user = cls.get_user_by_id(id)
        if user:
            print(user.__dict__)

    @classmethod
    def validate_user_test(cls):
        id = int(input("Id to fetch: "))
        email=input("email: ")
        password=input("password: ")
        user = cls.validate_user(userId=id, email=email, password=password)

        if user:
            print(user.__dict__)

    ##### TESTS STOP #############