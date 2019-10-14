import configparser
import psycopg2
from passlib.hash import pbkdf2_sha256
import json
# using raw python, we connect to the database and execute various user management roles

#role one assuming we have a UserDB created
class UserManager:
    def __init__(self,dbconfig=None, dbname=None):
        self.dbname = dbname or "UserDB"
        self.dbconfig = dbconfig or "database.ini" #Location of a configuration file

    def read_config(self):
        # read config file and save params
        parser = configparser.ConfigParser()
        parser.read(self.dbconfig)
        # create a dict of params
        # We read config section called postgresql
        section = 'postgresql'
        db_params = {}
        if parser.has_section(section):
            params  = parser.items(section)
            for item in params:
                db_params[item[0]] = item[1]
        else:
            raise Exception('postgresql section is not in the config file, check the spelling')
        return db_params 

    def connect(self):
        # connects to the database using the configurations given
        params = self.read_config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        return (connection, cursor)

    def encrypt_password(self, password):
        hash = pbkdf2_sha256.hash(password)
        return hash

    def verify_password(self, password, hash):
        return pbkdf2_sha256.verify(password,hash)

    def get_user(self, username):
        # check for the existance of the users
        sql = f"select * from users where users.username='{username}';"
        conn, cursor = self.connect()
        cursor.execute(sql)
        user = cursor.fetchone()
        cursor.close()
        if conn is not None:
            conn.close()
        return user

    def get_role_id(self, user_role):
        # Users table takes a foreign key of the id of the role
        sql = f"select role_id from user_roles where role_name='{user_role}';"
        conn, cursor = self.connect()
        cursor.execute(sql)
        id = cursor.fetchone()[0]
        cursor.close()
        if conn is not None:
            conn.close()
        return id

    def create_user(self,username, email, password,user_role, status = 'true'):
        # Call the db with new user info
        conn, cursor = self.connect()
        encrypted_password = self.encrypt_password(password)
        user = self.get_user(username)

        # check if the user is in the db
        if user is not None:
            return json.dumps({'error':'user already exists'})

        # Get the role id for users table
        try:
            role_id = self.get_role_id(user_role)
        except Exception as e:
            print("Invalid role",e)
        
        insert_query = f"INSERT INTO users(username, email, userpassword,userstatus,user_role) VALUES('{username}','{email}','{encrypted_password}',{status},{role_id})"
        try:
            cursor.execute(insert_query)
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(e)
        else:
            return json.dumps({"message":f"user {username} created successfully"})

    def generate_token(self,username):
        pass
        
    def authenticate(self, username, password):
        # We verify the username and password for user
        user = self.get_user(username)
        hash_password = user[3]
        verified = self.verify_password(password, hash_password)
        if verified:
            return json.dumps({"message":"logged in successfully"})
        else:
            return json.dumps({"error":f"invalid password for user {username}"})

        

if __name__ == "__main__":
    manager = UserManager()
    name = input("User: ")
    password = input("password:")
    print(manager.authenticate(name, password))
    

'''print("Create a User:\n")
    username = input("Username: ")
    email = input("\nEmail: ")
    password = input("Password:")
    user_role = input("Role, (administration,hr,accounts,support,customer service): ")
    print(manager.create_user(username,email,password, user_role))'''
