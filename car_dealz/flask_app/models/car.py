from sqlite3 import connect
from flask_app.__init__ import app
from flask_app.config.mysqlconnect import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import user
import re
bcrypt = Bcrypt(app)


class Car:
    db = "car_dealz"
    
    def __init__(self, data):
        self.id = data["id"]
        self.model = data["model"]
        self.make = data["make"]
        self.description = data["description"]
        self.year = data["year"]
        self.price = data["price"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data['user_id']
        self.user = None


    @classmethod
    def get_all_cars(cls):
        query = "SELECT * FROM car;"
        results = connectToMySQL('car_dealz').query_db(query)
        car_objects = []
        for row in results:
            car_objects.append(cls(row))
        print(results)
        return car_objects 
    
    @classmethod
    def get_by_id(cls, result_id):
        data = {"id": result_id}
        query = "SELECT * FROM car JOIN user on user.id = car.user_id WHERE car.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save_car(cls,data):
        query = '''INSERT INTO car (model, make, description, year, price, user_id) 
            VALUES (%(model)s,%(make)s,%(description)s,%(year)s,%(price)s,%(user_id)s);'''
        results = connectToMySQL("car_dealz").query_db(query,data)
        print(results)
        return results
    
    @staticmethod
    def validate_new_car(car):
        is_valid = True

        if len(car['make']) < 3:
            flash('Make must be at least 3 characters','car')
            is_valid = False
        
        if len(car['model']) < 3:
            flash('Must enter valid model name','car')
            is_valid = False
        
        if len(car['year']) <= 1:
            flash('Please choose a year','car')
            is_valid = False
        
        if len(car['price']) <= 1:
            flash('Must have price higher than $0','car')
            is_valid = False
        
        if len(car['description']) < 3:
            flash('Please enter a show description','car')
            is_valid = False
        return is_valid

    @classmethod
    def update_car(cls, truck):
        query = '''UPDATE car SET model = %(model)s, make = %(make)s, description = %(description)s,
                year = %(year)s, price = %(price)s WHERE id = %(id)s;'''
        results = connectToMySQL("car_dealz").query_db(query, truck)
        truck = cls.get_by_id(truck['id'])
        return results




    @classmethod
    def delete_car(cls, car_id):
        data = {"id": car_id}
        query = 'DELETE FROM car WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        return results

    @classmethod
    def carUser(cls,data):
        query = '''SELECT * FROM car LEFT JOIN user 
                ON car.user_id = user.id WHERE car.id = %(id)s;'''
        results = connectToMySQL(cls.db).query_db(query,data)
        print("carUser results", results)
        allCars = []
        for row in results:
            vehicle = cls(results[0])
            userData = {
                'id': row['user.id'],
                'firstName': row['firstName'],
                'lastName': row['lastName'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['user.created_at'],
                'updated_at': row['user.updated_at']
            }
            print('userdata', userData)
            oneUser = user.User(userData)
            vehicle.user = oneUser
            allCars.append(vehicle)
            print('allCars', allCars)
        return allCars
    
