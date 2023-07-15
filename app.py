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

    user_name = Column('username', String, primary_key=True)
    user_pwd = Column('password', String)

    def __init__(self, user_name, user_pwd):
        self.user_name = user_name
        self.user_pwd = user_pwd

    def __repr__(self):
        return f'\nUsername: {self.user_name}\n Password{self.user_pwd}'


class Passwords(Base):
    __tablename__ = 'passwords'

    password_id = Column('password_id', Integer, primary_key=True)
    website = Column('website', String)
    password = Column('password', String)
    user = Column(Integer, ForeignKey('users.username'))

    def __init__(self, pid, website, pwd, user):
        self.password_id = pid
        self.website = website
        self.password = pwd
        self.user = user

    def __repr__(self):
        return f'\n({self.password_id})\n{self.website}\n{self.password}\n{self.user}'


app = Flask(__name__)
engine = create_engine('sqlite:///project02.db')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

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


#@app.route('/create_password/<user>', methods=['POST', 'GET'])
@app.route('/create_password', methods=['POST', 'GET'])
def create_password():
    if request.method == 'POST':
        print(json.request)
        return render_template('passwordCreator.html', text='saved the password')
    return render_template('passwordCreator.html')

#@app.route('/randomPassword', methods=['POST'])
#def random_password():
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
    new_entry = Passwords(50000, website, 'Milton')
    try:
        session.add(new_entry)
        session.commit()
    except:
        i=1

@app.route('/password_store/<user>')
def password_store(user):
    # this is a test entry
    new_entry = Passwords(12345, 'https://codio.com', 'password', 'tochiboy')
    new_new_entry = Passwords(54321, 'https://youtube.com', '12345678', 'tochiboy')
    # adds the entries to the db
    try:
        session.add(new_entry)
        session.add(new_new_entry)
        session.commit()
    except:
        i = 1

    # finds only the entries with the correct username attached
    results = session.query(Passwords).where(Passwords.user == user)
    string = ''
    for r in results:
        string += f'{r}\n'
    # puts them all in one string and puts that on the show passwords
    return render_template('passwordStore.html', text=string)

@app.route('/show_password')
def show_password():
    random = "SELECT * FROM passwords "
    p = ''
    with engine.connect() as connection:   
        p = connection.execute(db.text(random))
        print(p.fetchall())
    return 'success'
   


# @app.route("/api", methods=["POST", "GET"])
# def api():
#     # print("backend grab form", request.form)
#     # print("backend grab form per: ", request.form.get('username'), request.form.get('password'))
#
#     username = request.form.get('username')
#     password = request.form.get('password')
#     print(username)
#
#     valid_users = session.query(Users).all()
#     if valid_users:
#         for user in valid_users:
#             if user.user_name == username:
#                 print("username already exists!")
#                 return jsonify(False)
#     new_entry = Users(username, password)
#     try:
#         session.add(new_entry)
#         session.commit()
#     except:
#         i = 1
#     return jsonify(f"Username {username} added!")

    # sql query to search for users with specific username
    # if username exits , return jsonify string stating username exists
    # if username in valid_users: # change to db name
    #     print("username already exists!")
    #     return jsonify(False)
    #
    # # If it doesn't exist in the set
    # # insert into db both username and password .
    # valid_users[username] = password
    # return jsonify(f"Username {username} added!")

    # flask redirect to passwordStore page  https://stackoverflow.com/questions/14343812/redirecting-to-url-in-flask
    # return redirect(url_for('password_store'))

    # https://flask-login.readthedocs.io/en/latest/



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
