#importing outside libraries for use in the project
from flask import Flask, session, redirect, url_for, escape, render_template, request, flash
import requests

#importing files that I created for the project
from user import *

#Setting up Flask
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #Recieving the information from the form from the user.
        username = request.form['username']
        password = request.form['password']
        #Creating the object that will represent the user.
        user = User(username)
        #Now checking to see if the user is in the database.
        flag = user.check(username, password)
        if flag == True:
            print(flag)
            #If the user is in the database, the user gets sent to the index page.
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            #If the user is not in the database then they will be sent to the
            #sign up page.
            return redirect(url_for('sign_up'))
    return render_template('login.html', title='Login Page')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        #Getting the correct data from the form that was submitted.
        username = request.form['username']
        password = request.form['password']
        password_check = request.form['second_password']
        if password != password_check:
            flash('The Passwords must match')
            return redirect(url_for('sign_up'))
        #Creating the object that will represent the user.
        user = User(username)
        #Encrypting the password
        password, hashed = user.encrypt_pass(password)
        #Adding the user to the database
        user.add(username, hashed)
        #Letting them into the index Page
        return redirect(url_for('index'))
    return render_template('sign_up.html', title='Sign Up Page')

@app.route('/index', methods=['GET', 'POST'])
def index():
    #This line will ensure that the user is logged in.
    if 'username' not in session:
        return redirect(url_for('login'))
    name = session['username']
    url = "https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=61d27504cb064eaf912be90e31803d5d"
    r = requests.get(url)
    response_dict = r.json()
    articles = response_dict['articles']
    length = len(response_dict['articles'])
    return render_template('index.html', title='Home Page', username = name, articles = articles)

@app.route('/no_match', methods=['GET', 'POST'])
def no_match():
    return render_template('no_match.html', title='Home Page')

# set the secret key. keep this really secret:
app.secret_key = 'n3A\xef(\xb0Cf^\xda\xf7\x97\xb1x\x8e\x94\xd5r\xe0\x11\x88\x1b\xb9'

#This line will actually run the app.
if __name__ == '__main__':
    app.run(debug=True)

# image = response_dict['articles'][0]['urlToImage']
# news_title = response_dict['articles'][0]['title']
# url = response_dict['articles'][0]['url']
