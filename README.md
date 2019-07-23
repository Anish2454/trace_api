# Trace
Trace is an app that allows users to "vote with their wallets" by connecting them to businesses and brands that align with their social, political, and ethical beliefs. 

Created for the News Corp Summer 2019 internship project.

## Table of contents
* [General Info](#general-info)
* [Built With](#built-with)
* [Techncial Documentation](#technical-documentation)
* [Project Status](#project-status)
* [Authors](#authors)

## General Info
Trace is an app created by the News Corp summer 2019 interns that allows users to vote with their wallets. Users create an account wherein they take quizes to gauge their support on issues like abortion, sustainability, poverty reduction, etc. Users can then see how their views align with businesses and brands. Alternatley, users can scan products to pull up issues on the brand that creates it. 

## Built With
* Flask - The API
* Factiva - The newswire
* Reel - The framework
* Python, HTML, MySQL - The languages

## Technical Documentation
   ### API Methods
  #### getData (db_name, company_name, mode)	
   Gets data on a specified company. 
##### @param 
	db_name - name of the database being accessed
	company_name - name of the company
	mode - if mode is ‘single’ one company’s leanings is accessed, if mode is ‘list’ every company’s leanings are accessed
##### @Return 
    payload - dictionary of either a single company and it’s category (key)leanings (value) or all companies and their  category (key)leanings (value)

#### getUserPref (user_name)	
  Gets the user’s stances on the issues.
##### @param 
	user_name - the username
##### @return 
    user_data - the user’s stances on the issues.
  
#### getCompanyList (db_name, user_name)	
  Helper function to match company preferences to user
##### @param 
    db_name - name of database
    user_name - name of user
##### @return
    sorted_data - JSON file of the user’s top ten company matches

#### check_account_exist (username)
    Helper method to check if a username exists
##### @param
    username - the user’s username
##### @return 
    Boolean - username exists or not

#### create_account (user_name, password)
  Creates a new user account.
##### @param
    user_name - the username for the new account
    password - the password for the new account
##### @return 
    Boolean - true is the account does not already exist

#### addData (username, abortion, anti_poverty, made_in_us, lgbtq_support, sustainable, animal_cruel, veteran_support, gun_control)
    Adds the user’s stances to their data after taking issue quizzes. 
##### @param
    username - the user’s username
    abortion - the user’s stance on abortion
    anti_poverty - the user’s stance on poverty reduction
    made_in_us -  the user’s stance on items made in the USA
    lgbtq_support -  the user’s stance on support for the LGBTQ community
    sustainable -  the user’s stance on sustainable business practices
    animal_cruelty -  the user’s stance on animal cruelty
    veteran_support -  the user’s stance on veteran support
    gun_control -  the user’s stance on gun control
##### @return 
    Boolean - data is added

### API Endpoints
#### /companies/company
    Get - Returns data on a specified company

#### /users/username
    Get - Returns a list of matching companies
  	Post - Takes in a password and authenticate username and password, returns 
    true if the user exists

#### /users/username/preferences    
    Get - returns the user’s preferences
    Post - takes in the user’s preferences 	

#### /users/createAccount	
    Post - Takes in a username and password and makes an account


## Project Status
Trace is in its MVP form.

## Authors
* **Ahmet Ay, Backend Engineer**  - AWS, User Database, MySQL Migration, API
* **Brooke Corso, Backend Engineer / Technical Writer** - User On-Boarding, Documentation
* **Anish Shenoy, Mobile Engineer** - Built the App, API
* **Dev Thakkar, Backend Engineer** - API, Fetcher, and Transformer
