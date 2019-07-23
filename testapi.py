#!/usr/local/bin/python3
from flask import Flask, redirect, url_for, request, jsonify
import json
import sqlite3
import os
from operator import itemgetter
from flask import render_template, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class CreateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    passwordConfirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

app = Flask(__name__)
app.secret_key = os.urandom(32)

#user_table = sqlite3.connect('user_table.db')
#user_crsr = user_table.cursor()

USER_TABLE = 'user_table.db'
COMPANY_TABLE = 'company_data.db'
LOGGEDIN = {"anish"}


def getData(db_name,company_name,mode):

   db_connection = sqlite3.connect(db_name)
   db_crsr = db_connection.cursor()
   db_name = "'%s'" % db_name
   search_key = "'%s'" % company_name
   payload = {}

   if mode == "single" :
      db_crsr.execute("SELECT * FROM " + db_name + "WHERE company = " + search_key + ";")
      data =  db_crsr.fetchall()
   elif mode == "list":
      db_crsr.execute("SELECT * FROM " + db_name + ";")
      data =  db_crsr.fetchall()

   for i in data:

      leanings = {}
      leanings['abortion'] = i[2]
      leanings['anti_poverty'] = i[3]
      leanings['made_in_usa'] = i[4]
      leanings['lgbtq_support'] = i[5]
      leanings['sustainable'] = i[6]
      leanings['animal_cruel'] = i[7]
      leanings['veteran_support'] = i[8]
      leanings['gun_control'] = i[9]

      payload[i[1]] = leanings

   db_connection.close()
   return payload

def getUserPref(user_name):
    db_connection = sqlite3.connect(USER_TABLE)
    db_crsr = db_connection.cursor()
    db_crsr.execute('SELECT * FROM "users" WHERE username = "' + user_name + '";')
    user_data = list(db_crsr.fetchone())[2:]
    db_connection.close()
    return user_data

#Helper function for matching company preferences to user
def getCompanyList(user_name):
  if checkLogin(user_name) == True:
    user_data = getUserPref(user_name)
    company_data = getData(COMPANY_TABLE, 0, "list")

    company_to_percent = {}
    for company in company_data:
        company_leanings = company_data[company]

        multiplied = []
        company_leanings_list = []
        for i in company_leanings:
            company_leanings_list.append(company_leanings[i])
        multiplied = [a*b for a,b in zip(company_leanings_list, user_data)]

        #this is sus, can get negative numbers
        percentage = abs(((sum(multiplied) / len(company_leanings)) * 100))

        company_to_percent[company] = percentage

    sorted_data = sorted(company_to_percent.items(), key=itemgetter(1), reverse=True)[:9]
    return jsonify(sorted_data)
  else:
    return "NOT LOGGED IN"

#No endpoint, just checks if a username exists (helper)
def check_account_exist(username):
    db_connection = sqlite3.connect(USER_TABLE)
    db_crsr = db_connection.cursor()
    command = "SELECT username FROM users WHERE username = ?"
    usernames = db_crsr.execute(command, (username,))
    for list_username in usernames:
        return list_username != None
    db_connection.close()
    return False

def create_account(user_name, password):
    if check_account_exist(user_name) == False:
      db_connection = sqlite3.connect(USER_TABLE)
      db_crsr = db_connection.cursor()
      command = "INSERT INTO 'users' (username, password) VALUES "+"('" + user_name + "'" + ",'" + password + "');"
      db_crsr.execute(command)
      db_connection.commit()
      db_connection.close()
      LOGGEDIN.add(user_name)
      return True
    else:
      return False

def addData(username, abortion,anti_poverty,made_in_us,lgbtq_support,sustainable,animal_cruel, veteran_support, gun_control):
   db_name = "'users'"
   db_connection = sqlite3.connect(USER_TABLE)
   db_crsr = db_connection.cursor()
   user = "'%s'" % username
#UPDATE 'users' SET abortion = 3 WHERE username = 'anish';

   db_crsr.execute("UPDATE" + db_name + "SET " + "abortion = " + str(abortion) + "," + "anti_poverty = " +
   str(anti_poverty) + "," + "made_in_us = " + str(made_in_us) + "," + "lgbtq_support = " + str(lgbtq_support) + "," +
   "sustainable = " + str(sustainable) + "," + "animal_cruel = " + str(animal_cruel) + "," + "veteran_support = " + str(veteran_support) + "," + "gun_control = " + str(gun_control) +
   " WHERE" + " username = " + user)
   db_connection.commit()
   db_connection.close()
   return True

def checkLogin(username):
  if username in LOGGEDIN:
    return True
  else:
    return False


#ENDPOINTS

'''
#COMPANY SEARCH
#Endpoint: /companies/<company>/
#Example:
   /companies/ADP:
   {"ADP":
        {
         "lgbtq_support": 0.0,
         "veteran_support": 1.0,
         "abortion": 1.0,
         "made_in_usa": 0.0,
         "animal_cruel": 0.0,
         "sustainable": 0.0,
         "gun_control": 0.0,
         "anti_poverty": 0.0
         }
    }
'''
@app.route('/companies/<company>', methods=['GET'])
def companySearch(company):
    #if checkLogin(username) == True:
    return json.dumps(getData('company_data.db', company,"single"))
    #else:
      #return redirect(url_for(users))

'''
Endpoint: /users/<username>
For GET requests:
    #Example Return:
    [
      [
        "Johnson & Johnson",
        37.5
      ],
      [
        "Amazon",
        37.5
      ],
      [
        "Morgan Stanley",
        37.5
      ],
      [
        "Boeing",
        37.5
      ],
      [
        "Accenture",
        37.5
      ],
      [
        "IBM",
        25.0
      ],
      [
        "Cisco Systems, Inc.",
        25.0
      ],
      [
        "Kaiser Permanente",
        25.0
      ],
      [
        "General Motors",
        25.0
      ]
    ]

For POST requests:
    Takes in a 'password' and authenticates username and password
    Returns True or False
'''
@app.route('/users/<username>', methods=['GET', 'POST'])
def users(username):
    if request.method == "GET":
        return getCompanyList(username)
    '''elif request.method == "POST":
        password = request.form["password"]
        if (not check_account_exist(username)):
            return redirect(url_for(createAccount))
        db_connection = sqlite3.connect(USER_TABLE)
        db_crsr = db_connection.cursor()
        command = "SELECT password FROM users WHERE username = ? "
        passdb = db_crsr.execute(command, (username, )).fetchone()
        db_connection.close()
        if password == passdb[0]:
          if username not in LOGGEDIN:
            LOGGEDIN.add(username)
            return "LOG IN SUCCESFUL"
          else:
            return "ALREADY LOGGED IN"
        else:
          return redirect(url_for('login')) #"PASSWORD INCORRECT"
    else:
      return "INVALID METHOD"'''


'''@app.route('/users/<username>/login', methods=['POST'])
def login():
    if request.method == 'POST':
      user_name = request.form['username']
      password = request.form['password']
      if username in LOGGED_IN:
        return redirect(url_for(users))
      else:
        db_connection = sqlite3.connect(USER_TABLE)
        db_crsr = db_connection.cursor()
        db_crsr.execute('SELECT * FROM "users" WHERE username = "' + user_name + '";')
        user_password = list(db_crsr.fetchone())[1]
        db_connection.close()
        if password == user_password:
          LOGGED_IN.add(user_name)
          return redirect(url_for(login))
        else:
          return redirect(url_for(login))'''


'''
Endpoint: /users/<username>/preferences/
For GET requests:
    #Example
    {
      "abortion": 1,
      "animal_cruel": 1,
      "anti_poverty": 1,
      "gun_control": 1,
      "lgbtq_support": -1,
      "made_in_us": 1,
      "sustainable": 0,
      "veteran_support": -1
    }
For POST requests:
    Takes in "abortion", "anti_poverty", "made_in_us", "lgbtq_support", "sustainable", "animal_cruel", "veteran_support", "gun_control"
    returns True or False
'''
@app.route('/users/<username>/preferences', methods=['GET', 'POST'])
def prefs(username):
  if checkLogin(username) == True:
    if request.method == "GET":
        user_list = getUserPref(username)
        topics = ["abortion", "anti_poverty", "made_in_us",	"lgbtq_support", "sustainable",	"animal_cruel", "veteran_support", "gun_control"]
        user_dict = {}
        for i in range(len(user_list)):
            user_dict[topics[i]] = user_list[i]
        return jsonify(user_dict)
    if request.method == "POST":
        abortion = request.form['abortion']
        anti_poverty = request.form['anti_poverty']
        made_in_us = request.form['made_in_us']
        lgbtq_support = request.form['lgbtq_support']
        sustainable = request.form['sustainable']
        animal_cruel = request.form['animal_cruel']
        veteran_support = request.form['veteran_support']
        gun_control = request.form['gun_control']
        return jsonify(addData(username, abortion,anti_poverty,made_in_us,lgbtq_support,sustainable,animal_cruel, veteran_support, gun_control))
  else:
    return redirect(url_for('login'))

'''
Endpoint: /users/createAccount
For POST requests:
    Takes in 'username' and 'password'
    Returns true or false
'''
@app.route('/users/createAccount', methods=['GET','POST'])
def createAccount():
  if request.method == 'POST':
    user_name = request.form['username']
    password = request.form['password']
    
    #leaninings from survey go under here / modify create_account function insert leanings

    if jsonify(create_account(user_name,password)) == False:
      return "USER CREATED SUCCCESSFULLY"
    else:
      return redirect('/users/'+user_name) # usercreated redirect to user homepage

  elif request.method == 'GET':
    form = CreateAccountForm() 
    return render_template('create.html', title='Create Account', form=form)
  else:
    return "INVALID METHOD"

@app.route('/users/<username>/logout', methods=['POST'])
def logout(username):
  if request.method == 'POST':
    if username in LOGGEDIN:
      LOGGEDIN.remove(username)
      return "LOGOUT SUCCESSFUL"
    else:
      return "USER NOT LOGGED IN"

@app.route('/users/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    user_name = request.form['username']
    password = request.form['password']
    if (not check_account_exist(user_name)):
      return redirect(url_for(createAccount))
    db_connection = sqlite3.connect(USER_TABLE)
    db_crsr = db_connection.cursor()
    command = "SELECT password FROM users WHERE username = ? "
    passdb = db_crsr.execute(command, (user_name, )).fetchone()
    db_connection.close()
    if password == passdb[0]:
      if user_name not in LOGGEDIN:
        LOGGEDIN.add(user_name)
        return redirect('/users/'+user_name) #"LOG IN SUCCESFUL"
      else:
        return redirect('/users/'+user_name) # "ALREADY LOGGED-IN"
    else:
      return redirect(url_for('login')) #"PASSWORD INCORRECT"

  elif request.method == 'GET':
    form = LoginForm() 
    return render_template('login.html', title='Sign In', form=form)

  else:
    return "INVALID METHOD"



if __name__ == "__main__":
   app.debug = True
   app.run()
