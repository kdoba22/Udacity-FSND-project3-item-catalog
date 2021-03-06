from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import jsonify
from flask import session as login_session
from flask import make_response
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from array import array
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import random
import string
import json
import requests


app = Flask(__name__)

# CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web'] \
#  ['client_id']
CLIENT_ID = json.loads(
	open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Item Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///catalogmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
db = DBSession()


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route("/")
@app.route("/catalog/")
def viewcatalog():
    categories = db.query(Category).all()
    lastitem = db.query(Item).order_by(Item.last_update.desc()).limit(10).all()
    return render_template('catalogApp.html',
                           categories=categories, latest_items=lastitem)


@app.route("/catalog/<int:category_id>/")
def viewcatalogItems(category_id):
    categories = db.query(Category).all()
    selectedCategory = db.query(Category).filter_by(id=category_id).one()
    items = db.query(Item).filter_by(category_id=category_id)
    return render_template('viewitems.html', categories=categories,
                           selectedCategory=selectedCategory,
                           items=items)


@app.route("/catalog/desc/<int:category_id>/<int:item_id>")
def itemdescription(category_id, item_id):
    description = db.query(Item).filter_by(category_id=category_id, id=item_id)
    return render_template('viewitemdescription.html',
                           description=description)


@app.route('/catalog/<int:category_id>/<category_name>/new',
           methods=['GET', 'POST'])
def newCatalogItem(category_id, category_name):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newItem = Item(
                      name=request.form['name'],
                      description=request.form['description'],
                      category_id=category_id,
                      user_id=login_session['username'])
        db.add(newItem)
        db.commit()
        flash("new item successfully entered")
        return redirect('/catalog')
    else:
        return render_template('newitem.html', category_id=category_id,
                               category_name=category_name)


# Edit catalog Item
@app.route('/catalog/<int:item_id>/edit/', methods=['GET', 'POST'])
def editCatalogItem(item_id):
    editedItem = db.query(Item).filter_by(id=item_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedItem.user_id != login_session['username']:
		return "<script>function myFunction() {alert('You are not authorized to\
        edit this item. Please create your own item in order to edit.');}\
        </script><body onload='myFunction()''>"
    if request.method == 'POST':
        editedItem.name = request.form['name']
        editedItem.description = request.form['description']
        db.add(editedItem)
        db.commit()
        flash("Item has been edited")
        return redirect('/catalog')
    else:
        return render_template('edititem.html', item=editedItem)


# Delete an item
@app.route('/catalog/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteCatalogItem(item_id):
    itemToDelete = db.query(Item).filter_by(id=item_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if itemToDelete.user_id != login_session['username']:
        return "<script>function myFunction() {alert('You are not authorized to\
        delete this Item. Please create your own Item in order to delete.');}\
        </script><body onload='myFunction()''>"
    if request.method == 'POST':
        db.delete(itemToDelete)
        db.commit()
        flash("Item has been deleted")
        return redirect(url_for('viewcatalog'))
    else:
        return render_template('deleteItem.html', item=itemToDelete)


# create a JSON endpoint for all items in a category
@app.route('/catalog/<int:category_id>/item/JSON/')
def itemJSON(category_id):
    category = db.query(Category).filter_by(id=category_id).one()
    items = db.query(Item).filter_by(category_id=category_id).all()
    return jsonify(Item=[i.serialize for i in items])


# User Helper Functions
def createUser(login_session):
    print ("createUser")
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    db.add(newUser)
    db.commit()
    user = db.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        respopnse.header['Content-Type'] = 'application/json'
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
    print (access_token)
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
        rsponse.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not matvch app's."), 401)
        print ("Tokens client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response
    print (login_session.get('access_token'))
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # store the access token in the session for layter username
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

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px;\
              -webkit-border-radius: 150px; -moz-border-radius: 150px;">'
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    print (access_token)
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps("Failed to revoke token for given user.", 400))
        response.headers['Content-Type'] = 'application/json'
        return response


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
