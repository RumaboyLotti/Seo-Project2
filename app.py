from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from flask_behind_proxy import FlaskBehindProxy
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random
import json
import sqlalchemy as db
Base = declarative_base()
from Password import *

class Users(Base):
    __tablename__ = 'users'

    user_name = Column('username', String, primary_key=True,autoincrement=True)
    user_pwd = Column('password', String)

    def __init__(self, user_name, user_pwd):
        self.user_name = user_name
        self.user_pwd = user_pwd

    def __repr__(self):
        return f'\nUsername: {self.user_name}\n Password{self.user_pwd}'


# Creating a class to represent a table in a database for storing passwords.
# The class inherits from the `Base` class, which is typically associated with an ORM (Object-Relational Mapping) library like SQLAlchemy.

class Passwords(Base):
    __tablename__ = 'passwords'

    # Defining the columns in the table
    password_id = Column('password_id', Integer, primary_key=True, autoincrement=True)
    website = Column('website', String)
    password = Column('password', String)
    user = Column(Integer, ForeignKey('users.username'))

    def __init__(self, website, pwd, user):
        # Initializing the object with the provided values
        self.website = website
        self.password = pwd
        self.user = user

    def __repr__(self):
        # Defining the string representation of the object
        return f'\n{self.website}\n{self.password}\n{self.user}'


#specifying  db connections 
app = Flask(__name__)
engine = create_engine('sqlite:///project02.db')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


#route to login and its methodolgy 
@app.route('/', methods=['POST', 'GET'])
def start_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(username)

        valid_users = session.query(Users).all()
        print(valid_users)
        if valid_users:
            for user in valid_users:
                if user.user_name == username:
                    if user.user_pwd == password:
                        return redirect(url_for('dashboard', user=username))
                    return render_template('startPage.html', text=f'username {username} already exists!')
        new_entry = Users(username, password)
        try:
            session.add(new_entry)
            session.commit()
        except:
            i = 1
        return redirect(url_for('dashboard', user=username))
    return render_template('startPage.html')


@app.route('/dashboard/<user>')
def dashboard(user):
    return render_template('dashboard.html', user=user)


@app.route('/create_password', methods=['POST', 'GET'])
def create_password():
    if request.method == 'POST':
        print(json.request)
        return render_template('passwordCreator.html', text='saved the password')
    return render_template('passwordCreator.html')


@app.route('/randomPassword', methods=['GET', 'POST'])
def random_password():
    length = int(request.form.get('len', 10))
    special = int(request.form.get('spec', 0))
    number = int(request.form.get('num', 0))
    upper = int(request.form.get('upper', 0))
    lower = int(request.form.get('lower', 0))

    password = Create_Password(length, special, number, lower, upper)
    return password

@app.route('/savedata', methods=['POST'])
def process_strings():
    website = request.form.get('web')
    password = request.form.get('pass')
    save_data(website, password)

def save_data(website, password):
    # Inserts the password into the database
    new_entry = Passwords( website, 'Milton')
    try:
        session.add(new_entry)
        session.commit()
    except:
        i=1

# @app.route('/password_store/<user>')
# def password_store(user):
#     # this is a test entry
#     new_entry = Passwords(12345, 'https://codio.com', 'password', 'tochiboy')
#     new_new_entry = Passwords(54321, 'https://youtube.com', '12345678', 'tochiboy')
#     # adds the entries to the db
#     try:
#         session.add(new_entry)
#         session.add(new_new_entry)
#         session.commit()
#     except:
#         i = 1

#     # finds only the entries with the correct username attached
#     results = session.query(Passwords).where(Passwords.user == user)
#     string = ''
#     for r in results:
#         string += f'{r}\n'
#     # puts them all in one string and puts that on the show passwords
#     return render_template('passwordStore.html', text=string)

# @app.route('/show_password')
# # define a route show password and from there slect all passwords from the database and display it
# def show_password():
#     random = "SELECT * FROM passwords "
#     p = 'asl'
#     # engine is a global variable linking to db and using the execute method to run the query 
#     with engine.connect() as connection:   
#         p = connection.execute(db.text(random))
#         print(p.fetchall())
#     return render_template('passwordStore.html', text = print(p))
   
@app.route('/password_store/<user>', methods=['GET'])
def show_password(user):
    session = Session()
    user_data = session.query(Users).filter_by(user_name=user).first()
    password = user_data.user_pwd if user_data else None
    session.close()
    return render_template('passwordStore.html', password=password)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
