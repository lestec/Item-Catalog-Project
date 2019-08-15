from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
# adding asc for names below
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User 
# New imports for oauth
from flask import session as login_session
import random, string
#step 5 oauth imports
##json formatted style stores your clientID, secret code and OAth parameters
from oauth2client.client import flow_from_clientsecrets
#run into error trying to exchange an auth code for access token
from oauth2client.client import FlowExchangeError
# comprehensive HTTP client library in Python
import httplib2
#JSON module provides an API for converting in memory in python objects to
##serialized representation 
import json
#method that converts the return value from a fx into a real response object
from flask import make_response
#an Apache 2.0 licenced HTTP library written in Python similar to urllib2
import requests

app = Flask(__name__)


#declare my client ID by referencing this client secrets file
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "ItemCatalogProject"

#Connect to DB and create DB session
engine = create_engine('sqlite:///kidsevents.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    #return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# google auth connect
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token received from client
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    #check to see if user is already logged in    
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    #need to add in after add user login 
     #ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'
    
     # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# User Helper Functions
#takes login_session as input and creates new user in DB
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

#if a user ID is passed into this method it returns user object associated
#with this ID #
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

#Will take an email address and return an ID # if that email address 
#belongs to a user in our DB, if not returns none
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# NOT SURE but think need disconnect for email user too!

# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user
    access_token = login_session.get('access_token')
    #not sure if should change access_token line
    #print 'In gdisconnect access token is %s', access_token
    #print 'User name is: ' 
    #print login_session['username']
    if access_token is None:
    #print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    #not sure if leave below line or change
    #url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']    
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    #print 'result is '
    #print result
    if result['status'] == '200':
        #reset the user's session
        del login_session['access_token'] 
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
    #seeing if redirect works with google    
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        #response = redirect(url_for('showCatalog'))
        #flash("You are now logged out.")
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Show all catalog venues
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    category = session.query(Category).order_by(asc(Category.name)).all()
#going to differentiate whether a user is loggin in or not logged in 
#since the only option on this pg is to create a new rest     
    #if 'username' not in login_session:
    #    return render_template('publicCatalog.html', category=category)
    #else:
    #    return render_template('catalog.html', category=category)

    
    return render_template('catalog.html', category=category)
    #return "this page will show all my venues


#if the user click on one category, show the items for the picked category
#on the main pg. return 2 diff html templates based on user status
# create a new category venue
# wking: http://localhost:5000/catalog/new/
@app.route('/catalog/new/', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCategory = Categories(name=request.form['name'], user_id=login_session['user_id'])
        session.add(newCategory)
        flash('New Category %s Succesfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCatalog'))
    else:   
            return render_template('newCategory.html')
    #return "this pg is for making new category"


@app.route('/catalog/<int:category_id>/')
@app.route('/catalog/<int:category_id>/items/')
def itemsMenu(category_id):
    #categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('itemsCatalog.html', category=category, items=items)
    

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
