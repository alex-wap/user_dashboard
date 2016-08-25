from system.core.model import Model
import bcrypt, re

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def get_users(self):
        query = "SELECT * from users"
        return self.db.query_db(query)

    def get_user(self,id):
        query = "SELECT * from users where id = :id LIMIT 1"
        data = {'id':id}
        return self.db.query_db(query, data)

    def login_user(self, data):
        password = data['password']
        user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
        user_data = {'email': data['email']}
        # same as query_db() but returns one result
        user = self.db.query_db(user_query, user_data)
        if user:
           # check_password_hash() compares encrypted password in DB to one provided by user logging in
            if self.bcrypt.check_password_hash(user[0]['password'], password):
                return user
        # Whether we did not find the email, or if the password did not match, either way return False
        return False

    def create_user(self,form):
        data = {
            'email': form['email'],
            'first_name': form['first_name'],
            'last_name': form['last_name'],
            'password': form['password'],
            'confirm' : form['confirm']
        }
        # make first user an admin
        sql_first = "SELECT * from users LIMIT 1"
        first_user = self.db.query_db(sql_first)
        if first_user == []:
            data['user_level'] = 'admin'
        else:
            data['user_level'] = 'normal'
        # validation
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        if not data['first_name']:
            errors.append('First Name cannot be blank')
        elif len(data['first_name']) < 2:
            errors.append('First name must be at least 2 characters long')
        elif not data['first_name'].isalpha():
            errors.append('First name must be letters only')
        if not data['last_name']:
            errors.append('Last name cannot be blank')
        elif len(data['last_name']) < 2:
            errors.append('Last name must be at least 2 characters long')
        elif not data['last_name'].isalpha():
            errors.append('Last name must be letters only')
        if not data['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(data['email']):
            errors.append('Email format must be valid!')
        if not data['password']:
            errors.append('Password cannot be blank')
        elif len(data['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif data['password'] != data['confirm']:
            errors.append('Password and confirmation must match!')
        # If we hit errors, return them, else return True.
        if errors:
            return {"status": False, "errors": errors}
        else:
            # check if email already in db
            user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
            user_data = {'email': data['email']}
            user = self.db.query_db(user_query, user_data)
            if user:
                errors.append('Email is already in the system!')
                return {"status": False, "errors": errors}
            # insert user
            password = data['password']
            hashed_pw = self.bcrypt.generate_password_hash(password)
            data['password'] = hashed_pw
            sql = '''INSERT INTO users (first_name, last_name, email, password, user_level, created_at)
                 VALUES (:first_name, :last_name, :email, :password, :user_level, NOW())'''
            self.db.query_db(sql, data)
            # Then retrieve the last inserted user.
            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            users = self.db.query_db(get_user_query)
            print errors
            return { "status": True, "user": users[0] }

    def update_user(self,data):
        if data['update'] == 'email':
            if data['user_level']=='normal' or data['user_level']=='admin':
                query = '''UPDATE users SET email=:email, first_name=:first_name, last_name=:last_name, user_level=:user_level 
                        WHERE id=:id'''
            else:
                query = '''UPDATE users SET email=:email, first_name=:first_name, last_name=:last_name 
                        WHERE id=:id'''
        elif data['update'] == 'password':
            # update password
            password = data['password']
            hashed_pw = self.bcrypt.generate_password_hash(password)
            data['password'] = hashed_pw
            query = '''UPDATE users SET password=:password WHERE id=:id'''
        elif data['update'] == 'description':
            # update description
            query = '''UPDATE users SET description=:description WHERE id=:id'''
        return self.db.query_db(query, data)
    
    def grab_messages(self):
        query = "SELECT * from messages where users_id = :user_id"
        data = {'user_id':1}
        return self.db.query_db(query, data)

    def destroy_user(self, id):
        query = "DELETE FROM users where id = :id LIMIT 1"
        data = {"id" : id }
        self.db.query_db(query,data)
        return True
