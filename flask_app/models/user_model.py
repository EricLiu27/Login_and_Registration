from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
import re
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data ['email']
        self.password = data ['password']
        self.created_at = data ['created_at']
        self.updated_at = data ['updated_at']


    @classmethod
    def create(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s, %(password)s);"
        
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def get_by_id (cls,data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def get_by_email (cls,data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    @staticmethod
    def is_valid (data):
        is_valid = True
        #first name validation
        if len(data['first_name']) < 1:
            flash('First name is required', 'reg')
            is_valid = False
        elif len(data['first_name']) < 2:
            flash('First name must be 2 characters at least', 'reg')
            is_valid = False
        elif not data ['first_name'].isalpha():
            flash('First name can only contain letters', 'reg')
            is_valid = False
        #last name validation
        if len(data['last_name']) < 1:
            flash('Last name required', 'reg')
            is_valid = False
        elif len(data['last_name']) < 2:
            flash('Last name must be 2 characters at least', 'reg')
            is_valid = False
        elif not data ['last_name'].isalpha():
            flash('Last name can only contain letters', 'reg')
            is_valid = False
        #email validation
        if len(data['email']) < 1:
            flash('Email required', 'reg')
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']):
            flash('Email must be in proper format','reg')
            is_valid = False
        else: #check to see if email is already in the database
            potential_user = User.get_by_email({'email':data['email']})
            if potential_user:
                flash('Email already exists in db', 'reg')
                is_valid=False
        #password validation
        if len(data['password']) < 1:
            is_valid=False
            flash('password required','reg')
        elif len(data['password']) < 8:
            is_valid=False
            flash('password must be 8 characters or more','reg')
        elif data ['password'] != data['cpass']:
            is_valid=False
            flash('password must match','reg')
        return is_valid
        