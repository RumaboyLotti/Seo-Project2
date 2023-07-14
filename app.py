from flask import Flask, render_template, url_for, flash, redirect
from flask_behind_proxy import FlaskBehindProxy

app = Flask(__name__)

@app.route('/')
def start_page():
    return render_template('startPage.html')

@app.route('/create_password')
def create_password():
    return render_template('passwordCreator.html')

@app.route('/password_store')
def password_store():
    return render_template('passwordStore.html')


@app.route("/api", methods=["POST"])
def api():
    # print("backend grab form", request.form)
    # print("backend grab form per: ", request.form.get('username'), request.form.get('password'))

    username = request.form.get('username')
    password = request.form.get('password')

    # sql query to search for users with specific username
    # if username exits , return jsonify string stating username exists
    if username in valid_users: # change to db name
        print("username already exists!")
        return jsonify(False) 
    
    # If it doesn't exist in the set
    # insert into db both username and password .
    valid_users.add(username)
    return jsonify(f"Username {username} added!")

    #flask redirect to passwordStore page  https://stackoverflow.com/questions/14343812/redirecting-to-url-in-flask 
    # return redirect(url_for('password_store'))

    # https://flask-login.readthedocs.io/en/latest/ 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
