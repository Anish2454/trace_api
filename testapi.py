from flask import Flask, redirect, url_for, request, jsonify
import json
import sqlite3
import os
from operator import itemgetter

app = Flask(__name__)
app.secret_key = os.urandom(32)


#user_table = sqlite3.connect('user_table.db')
#user_crsr = user_table.cursor()

USER_TABLE = 'user_table.db'
COMPANY_TABLE = 'company_data.db'


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

#Helper function for matching company preferences to user
def getCompanyList(db_name, user_name):
    db_connection = sqlite3.connect(USER_TABLE)
    db_crsr = db_connection.cursor()
    db_crsr.execute('SELECT * FROM "users" WHERE username = "' + user_name + '";')
    user_data = list(db_crsr.fetchone())[2:]
    db_connection.close()

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

#ENDPOINTS

'''
#COMPANY SEARCH
#Endpoint: /companies
#Takes in 'company_name'
#Example Return:
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
@app.route('/companies', methods=['GET', 'POST'])
def companySearch():

   if request.method == 'POST':

      company_name = request.form['company_name']

      return json.dumps(getData('company_data.db', company_name,"single"))

   else:

      return "err"


'''
#Returns a list of top 10 companies and perecntages of how much they match to you
#Endpoint: /users/companyList
#Takes in 'username'
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
'''
@app.route('/users/companyList', methods=['GET', 'POST'])
def companyList():
   if request.method == 'POST':

      user_name = request.form['username']

      return getCompanyList('user_table.db', user_name)

   else:

      return "err"

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

'''
Endpoint: /users/auth
Takes in 'username' and 'password'
Returns either True or False
'''
@app.route('/users/auth', methods=['GET', 'POST'])
def auth():
    username = request.form['username']
    password = request.form['password']
    if (not check_account_exist(username)):
        return jsonify(False)
    db_connection = sqlite3.connect(USER_TABLE)
    db_crsr = db_connection.cursor()
    command = "SELECT password FROM users WHERE username = ? "
    passdb = db_crsr.execute(command, (username, )).fetchone()
    db_connection.close()
    return jsonify(password == passdb[0])

@app.route('/users/createAccount', methods=['GET', 'POST'])
def createAccount(user_name,password):

    #switch to json http get/post
    #success fail message =

    return "success fail message"

if __name__ == "__main__":
   app.debug = True
   app.run()
