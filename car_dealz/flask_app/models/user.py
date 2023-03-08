from sqlite3 import connect
from flask_app.__init__ import app
from flask_app.config.mysqlconnect import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import car
import re

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db="car_dealz"
    
    def __init__(self,data):
        self.id=data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.car = []


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        print("query check")
        results = connectToMySQL(cls.db).query_db(query,data)
        print("results check")
        if len(results) < 1:
            return False
        print(results)
        return cls(results[0])

    @classmethod
    def get_password(cls,data):
        query = "SELECT user.password FROM user WHERE email = %(email)s;"
        results = connectToMySQL("car_dealz").query_db(query,data)
        print(results)
        return results

    @staticmethod
    def validate_register(register):
        valid = True
        query = "SELECT * FROM user WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,register)
        if len(register["first_name"]) < 2:
            valid = False
            flash("First name must be at least 2 characters.","register")
        if len(register["last_name"]) < 2:
            valid = False
            flash("Last name must be at least 2 characters.","register") 
        if len(register["email"]) == 0 or not EMAIL_REGEX.match(register['email']): 
            flash("Invalid email address!","register")
            valid = False
        if len(results) >=1:
            flash("An account with that email already exists, please log in.","register")
            valid = False
        if register["password"] != register["confirm"]:
            flash("Passwords must match","register")
            valid = False
        if len(register['password']) < 8:
            flash("Password must be at least 8 characters","register")
            valid= False
        return valid   

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM user WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        print(results)
        return cls(results[0])

    @classmethod
    def save_user(cls, data):
        query = '''INSERT INTO user (first_name, last_name, email, password)
                VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);'''
        results = connectToMySQL(cls.db).query_db(query,data)
        return results

    @classmethod
    def get_user_car(cls,data):
        query = "SELECT * from user LEFT JOIN car on user.id = car.user_id WHERE user.id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        user = cls(result[0])
        for row in result:
            carData = {
                'id': row['car.id'],
                'model': row['model'],
                'make': row['make'],
                'description': row['description'],
                'year': row['year'],
                'price': row['price'],
                'user_id': row['user_id']
            }
            user.car.append(car.Car(carData))
        return user 

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM user;'
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users