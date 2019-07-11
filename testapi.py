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

    sorted_data = sorted(company_to_percent.items(), key=itemgetter(1), reverse=True)
    return jsonify(sorted_data)

#ENDPOINTS

#COMPANY SEARCH
@app.route('/companies', methods=['GET', 'POST'])
def companySearch():

   if request.method == 'POST':

      company_name = request.form['company_name']

      return json.dumps(getData('company_data.db', company_name,"single"))

   else:

      return "err"


# USERS /users/<user name>/companies/: -> returns -list of companies containing name, leanings percentage, logo link
#                                                               [ { "name":"apple", "leanings" : { "issue1": "support"} ... } .... ]
@app.route('/users/companylist', methods=['GET', 'POST'])
def companyList():
   if request.method == 'POST':

      user_name = request.form['user_name']

      return getCompanyList('user_table.db', user_name)

   else:

      return "err"




# /users/createaccount/<username>/<password>/: -> takes in username, email, password, survey answers and creates user on the backend
@app.route('/users/createAccount', methods=['GET', 'POST'])
def createAccount(user_name,password):

    #switch to json http get/post
    #success fail message =

    return "success fail message"



# /users/<username>/friends/: -> returns list of friends and their leanings
@app.route('/users/<user_name>/friends')
def friends(user_name):

    #friends_table_data =  function to gather friends data from table

    return "friends_table_data"

if __name__ == "__main__":
   app.debug = True
   app.run()
