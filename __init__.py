""" 
    Project.py

    * Programmed by Guillaume Simler
    * Main program of this application: 
        - the web server is set up
        - the methods (GET/POST) are defined

    More information in the comments and/or README File
"""

"""
    I. Module imports
"""

# 1. Flask: manages the templates

from flask import Flask, render_template, request, redirect, jsonify
from flask import url_for, flash, make_response
from flask import session as login_session

# 2. SQL Alchemy: manages the database

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Art, Artist, Artwork, Picture, User

# 3. oauth2client: Manages the authorization &authentication processes

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

# 4. Helper modules

import random
import string
import httplib2
import json


# 5. Security

from security import escape, generate_token

"""
    II. Initizalization
"""

# 1. Define app
app = Flask(__name__)

# 2. Connect to Database and create database session

engine = create_engine('sqlite:///artcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# 3. Load Client Secret File (Google)

CLIENT_ID = json.loads(
open('google_secrets.json', 'r').read())['web']['client_id']


"""
    IV. login 
"""
# 1. get the login window

@app.route('/login/')
def showLogin():
    state = generate_token()
    login_session['state'] = state

    return render_template('login.html', state = state)


#2. google connect

@app.route('/gconnect', methods=['POST'])
def gconnect():

    # 1. Check for the server token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid server side token'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response


    # 2. Upgrade the client token
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('google_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the auth code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # 3. Check the client token
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')),500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # 4. Check the name matching
    gplus_id = credentials.id_token['sub']

    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID issuer doesn't match the issuer"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response   


    # 5. Verify that the access token is valid for this app

    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID doesn't match app's"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')


    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response =  make_response(json.dumps('current user is already connected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response


    # store the access token value and the user info

    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']


    # see if user exists, if it doesn't make a new one:
    user_id = getUserID(login_session['email']) 
    if not user_id:
        user_id = createUser(login_session)

    login_session['user_id']= user_id


    output = "<h1>Hello, %s</h1>" %login_session['username']
    output += "<h2>You're logged in and will be redirected ... </h2>"

    return output


@app.route('/logout')
def startLogout():
    del login_session['user_id']
    del login_session['username'] 
    del login_session['email']
    del login_session['gplus_id']
    del login_session['credentials']
    
        
    flash("You've been logged out")

    return redirect(url_for('showArtCatalog'))


"""
    IV. Main program
"""

# IV.1 JSON Gateways
#
# Enables the extraction of the data in JSON
# Please read the discussion about main and secondary
# data in the README

# IV.1.1. Generic JSON requests


@app.route('/arts/JSON/')
def json_arts():
    arts = session.query(Art).all()
    return jsonify(arts=[art.serialize for art in arts])

@app.route('/artists/JSON/')
def json_artists():
    artists = session.query(Artist).all()
    return jsonify(artists=[artist.serialize for artist in artists])

@app.route('/artworks/JSON/')
def json_artworks():
    artworks = session.query(Artwork).all()
    return jsonify(artworks=[artwork.serialize for artwork in artworks])

    # IV.1.2. Specific JSON request
@app.route('/arts/<int:art_id>/JSON/')
def json_arts_spe(art_id):
    art = session.query(Art).filter_by(id = art_id).one()
    return jsonify(art=[art.serialize])

@app.route('/artists/<int:artist_id>/JSON/')
def json_artists_spe(artwork_id):
    artist = session.query(Artist).filter_by(id = artist_id).one()
    return jsonify(artists=[artist.serialize])

@app.route('/artworks/<int:artwork_id>/JSON/')
def json_artworks_spe(artwork_id):
    artwork = session.query(Artwork).filter_by(id = artwork_id).one()
    return jsonify(artworks=[artwork.serialize])


@app.route('/artworks/<int:artwork_id>/pictures/JSON')
def json_pictures_spe(artwork_id):
    pictures = session.query(Picture).filter_by(artwork_id=artwork_id).all()
    return jsonify(pictures=[picture.serialize for picture in pictures])


# IV.2. Display/read elements
#
# This will display the elements

@app.route('/')
@app.route('/catalog/')
def showArtCatalog():
    # get data
    arts = session.query(Art).all()
    pictures = getFrontImage(arts)
    artists = session.query(Artist).all()

    return render_template('catalog.html',
                           arts=arts,
                           pictures=pictures,
                           artists=artists,
                           login_session = login_session)


@app.route('/art/<int:art_id>/')
def showArts(art_id):

    arts = session.query(Art).all()
    artworks = session.query(Artwork).filter_by(art_id=art_id).all()

    return render_template('arts.html',
                           arts=arts,
                           id=art_id,
                           artworks=artworks,
                           login_session = login_session)


@app.route('/artist/<int:artist_id>/')
def showArtists(artist_id):
    artists = session.query(Artist).all()

    pictures = session.query(Artwork.name.label('Name'),
                             Artwork.id.label('id'),
                             Picture.filename.label('filename'),
                             Picture.photographer.label('photographer')).filter(Artwork.artist_id == artist_id).join(Picture).all()

    return render_template('artists.html',
                           artists=artists,
                           artist_id=artist_id,
                           pictures=pictures,
                           login_session = login_session)


@app.route('/artworks/<int:artwork_id>')
def showArtworks(artwork_id):
    artwork = session.query(Artwork).filter_by(id=artwork_id).one()
    pictures = session.query(Picture).filter_by(artwork_id=artwork_id).all()
    artist = session.query(Artist).filter(Artwork.id == artwork_id).join(Artwork).one()

    return render_template('artworks.html',
                           artwork=artwork,
                           pictures=pictures,
                           artwork_id=artwork_id,
                           artist=artist,
                           login_session = login_session)


# IV.3 Edit/Update elements
#
# This enables the update of elements

@app.route('/art/<int:art_id>/edit/', methods=['GET', 'POST'])
def editArt(art_id):
    if not checkLogin():
        return redirect(url_for('showArts', art_id = art_id)) 
    
    if not checkUser(Art, art_id):
        return redirect(url_for('showArts', art_id = art_id))     

    art = session.query(Art).filter_by(id=art_id).one()

    if request.method == 'POST':
        edited_type = request.form['type']
        edited_description = request.form['description']

        art.type = edited_type
        art.description = edited_description

        session.commit()

        message_update('art', edited_type)

        return redirect(url_for('showArts', art_id=art_id))
    else:
        return render_template('art_edit.html', 
                                art=art,
                                login_session = login_session)


@app.route('/artworks/<int:artwork_id>/edit/', methods=['GET', 'POST'])
def editArtwork(artwork_id):
    if not checkLogin():
        return redirect(url_for('showArtworks', artwork_id = artwork_id))

    if not checkUser(Artwork, artwork_id):
        return redirect(url_for('showArtworks', artwork_id = artwork_id))
    
    artwork = session.query(Artwork).filter_by(id=artwork_id).one()

    if request.method == 'POST':

        # Enable the input of a new ART Discipline
        if request.form['new_art'] == 'False':
            artwork.art_id = request.form['art_id']
        else:
            new_value = request.form['add_art']

            # Create the new art entry
            new_Art = Art(type=new_value, user_id=1)
            session.add(new_Art)
            session.commit()

            message_create('art', new_value)

            # Get the new art id

            new_art = session.query(Art).filter_by(type=new_value).one()
            artwork.art_id = new_art.id

        # Enable the input of a new ARTIST
        if request.form['new_artist'] == 'False':
            artwork.artist_id = request.form['artist_id']
        else:
            new_value = request.form['add_artist']

            # Create the new art entry
            new_Artist = Artist(name=new_value, user_id=1)
            session.add(new_Artist)
            session.commit()

            message_create('artist', new_value)

            # Get the new art id

            new_artist = session.query(Artist).filter_by(name=new_value).one()
            artwork.art_id = new_artist.id

        artwork.name = request.form['name']
        artwork.description = request.form['description']
        artwork.purchase_year = request.form['purchase_year']
        artwork.size = request.form['size']
        artwork.weight = request.form['weight']
        artwork.purchase_prize = request.form['purchase_prize']

        # !!!!!!!!! Image Handling !!!!!!!!!

        # Delete the pictures
        targetedpictures = getList(request.form['delete_picture'])

        print targetedpictures

        if targetedpictures[0]:
            for targetedpicture in targetedpictures:
                target = session.query(Picture).filter_by(
                    id=int(targetedpicture)).one()
                session.delete(target)

        # ///////// Image Handling /////////

        session.commit()

        message_update('artwork', artwork.name)

        return redirect(url_for('showArtworks', artwork_id=artwork_id))

    else:
        arts = session.query(Art).all()
        artists = session.query(Artist).all()

        return render_template('artwork_edit.html',
                               artwork=artwork,
                               arts=arts,
                               artists=artists,
                               login_session = login_session)


@app.route('/artists/<int:artist_id>/edit/', methods=['GET', 'POST'])
def editArtist(artist_id):
    if not checkLogin():
        return redirect(url_for('showArtists', artist_id = artist_id)) 

    if not checkUser(Artist, artist_id):
        return redirect(url_for('showArtists', artist_id = artist_id)) 

    artist = session.query(Artist).filter_by(id=artist_id).one()

    if request.method == 'POST':
        artist.name = request.form['name']
        artist.information = request.form['information']
        artist.url = request.form['url']

        session.commit()

        message_update('artist', artist.name)

        return redirect(url_for('showArtists', artist_id=artist_id))
    else:
        return render_template('artist_edit.html', 
                               artist=artist,
                               login_session = login_session)


# IV.4 add elements
#
# This enables the addition of elements

@app.route('/art/new/', methods=['GET', 'POST'])
def addArt():
    # Placeholder for the user
    if not checkLogin():
        return redirect(url_for('showArtCatalog')) 
    
    # There is no risk of error as the existence of login_session['user_id']
    # was checked by checkLogin()
    user = login_session['user_id']

    if request.method == 'POST':
        new_type = request.form['type']
        new_description = request.form['description']

        new_Art = Art(type=new_type,
                      description=new_description,
                      user_id=user)

        session.add(new_Art)
        session.commit()

        message_create('art', new_type)

        new_id = session.query(Art).filter_by(type=new_type).one()

        return redirect(url_for('showArts', art_id=new_id.id))
    else:
        return render_template('art_add.html',
                               login_session = login_session)


@app.route('/artworks/new/', methods=['GET', 'POST'])
def addArtwork():
    if not checkLogin():
        return redirect(url_for('showArtCatalog')) 

    if request.method == 'POST':
        # There is no risk of error as the existence of login_session['user_id']
        # was checked by checkLogin()
        user = login_session['user_id']

        # Enable the input of a new ART Discipline
        if request.form['new_art'] == 'False':
            new_art_id = request.form['art_id']
        else:
            new_value = request.form['add_art']

            # Create the new art entry
            new_Art = Art(type=new_value, user_id=user)
            session.add(new_Art)
            session.commit()

            message_create('art', new_value)

            # Get the new art id

            new_art = session.query(Art).filter_by(type=new_value).one()
            new_art_id = new_art.id

        # Enable the input of a new ARTIST
        if request.form['new_artist'] == 'False':
            new_artist_id = request.form['artist_id']
        else:
            new_value = request.form['add_artist']

            # Create the new art entry
            new_Artist = Artist(name=new_value, user_id=user)
            session.add(new_Artist)
            session.commit()

            message_create('artist', new_value)
            # Get the new art id

            new_artist = session.query(Artist).filter_by(name=new_value).one()
            new_artist_id = new_artist.id

        # Get the other input fields
        new_name = request.form['name']
        new_description = request.form['description']
        new_purchase_year = request.form['purchase_year']
        new_size = request.form['size']
        new_weight = request.form['weight']
        new_purchase_prize = request.form['purchase_prize']

        # Create the new entry
        new_artwork = Artwork(name=new_name,
                              description=new_description,
                              purchase_year=new_purchase_year,
                              size=new_size,
                              weight=new_weight,
                              purchase_prize=new_purchase_prize,
                              user_id=user,
                              art_id=new_art_id,
                              artist_id=new_artist_id)
        session.add(new_artwork)
        session.commit()

        # Get the new id

        new_artwork_id = session.query(Artwork).filter_by(name=new_name).one()

        message_create('artworks', new_name)

        return redirect(url_for('showArtworks', artwork_id=new_artwork_id.id))

    else:
        arts = session.query(Art).all()
        artists = session.query(Artist).all()

        return render_template('artwork_add.html', 
                               arts=arts, 
                               artists=artists,
                               login_session = login_session)


@app.route('/artists/new/', methods=['GET', 'POST'])
def addArtist():
    if not checkLogin():
        return redirect(url_for('showArtCatalog')) 

    # There is no risk of error as the existence of login_session['user_id']
    # was checked by checkLogin()
    user = login_session['user_id']

    if request.method == 'POST':
        new_name = request.form['name']
        new_information = request.form['information']
        new_url = request.form['url']

        new_artist = Artist(name=new_name,
                            information=new_information,
                            url=new_url,
                            user_id=user)
        session.add(new_artist)
        session.commit()

        new_artist_id = session.query(Artist).filter_by(name=new_name).one()

        message_create('artist', new_name)

        return redirect(url_for('showArtists', artist_id=new_artist_id.id))
    else:
        return render_template('artist_add.html',
                               login_session = login_session)


# IV.5 delete elements
#
# This enables the deletion of elements

@app.route('/art/<int:art_id>/delete/', methods=['GET', 'POST'])
def deleteArt(art_id):

    # Safety checks
    if not checkLogin():
        return redirect(url_for('showArts', art_id = art_id))

    if not checkUser(Art, art_id):
        return redirect(url_for('showArts', art_id = art_id))
        
        

    art = session.query(Art).filter_by(id=art_id).one()
    artworks = session.query(Artwork).filter_by(art_id=art_id).all()
    pictures = session.query(Artwork.id, Picture.id, Picture.filename).filter_by(
        art_id=art_id).join(Picture).all()

    nb = []
    nb.append(len(artworks))
    nb.append(len(pictures))

    if request.method == 'POST':

        for artwork in artworks:
            session.delete(artwork)

        for picture in pictures:
            pic = session.query(Picture).filter_by(id=picture[1]).one()
            session.delete(pic)

        session.delete(art)
        session.commit()

        message_delete('art', art.type)
        return redirect(url_for('showArtCatalog'))
    else:
        return render_template('art_delete.html',
                               art=art,
                               artworks=artworks,
                               nb=nb,
                               login_session = login_session)


@app.route('/artworks/<int:artwork_id>/delete/', methods=['GET', 'POST'])
def deleteArtwork(artwork_id):
    if not checkLogin():
        return redirect(url_for('showArtworks', artwork_id = artwork_id)) 

    if not checkUser(Artwork, artwork_id):
        return redirect(url_for('showArtworks', artwork_id = artwork_id)) 

    artwork = session.query(Artwork).filter_by(id=artwork_id).one()
    pictures = session.query(Picture).filter_by(artwork_id=artwork_id).all()

    nb = len(pictures)

    if request.method == 'POST':

        for picture in pictures:
            session.delete(picture)

        session.delete(artwork)
        session.commit()

        message_delete('artwort', artwork.name)

        return redirect(url_for('showArtCatalog'))
    else:
        return render_template('artwork_delete.html', 
                               artwork=artwork,
                               nb=nb,
                               login_session = login_session)


@app.route('/artists/<int:artist_id>/delete/', methods=['GET', 'POST'])
def deleteArtist(artist_id):
    if not checkLogin():
        return redirect(url_for('showArtists', artist_id = artist_id))

    if not checkUser(Artist, artist_id):
        return redirect(url_for('showArtists', artist_id = artist_id))

    artist = session.query(Artist).filter_by(id=artist_id).one()
    artworks = session.query(Artwork).filter_by(artist_id=artist_id).all()
    pictures = session.query(Artwork.artist_id, Picture.id, Picture.filename).filter_by(
        artist_id=artist_id).join(Picture).all()

    nb = []
    nb.append(len(artworks))
    nb.append(len(pictures))

    if request.method == 'POST':

        for artwork in artworks:
            session.delete(artwork)

        for picture in pictures:
            pic = session.query(Picture).filter_by(id=picture[1]).one()
            session.delete(pic)

        session.delete(artist)
        session.commit()

        message_delete('artist', artist.name)
        return redirect(url_for('showArtCatalog'))
    else:
        return render_template('artist_delete.html', 
                               artist=artist, 
                               artworks=artworks, 
                               nb=nb,
                               login_session = login_session)

"""
    V. Helper functions
"""


def getFrontImage(arts):
    """
        Returns two random pictures from a list
    """
    result = []

    for art in arts:

        pictures = session.query(Picture, Artwork.art_id).filter(Artwork.art_id == art.id).join(Artwork).all()
        
        if pictures:
            nb = len(pictures) - 1
            target = random.randint(0, nb)
            result.append(pictures[target].Picture)

        else:
            result.append('blank')

    return result


def message_update(type, value):
    """
        Creates two messages respectively for the back (print) and the front end (flash())
        Gets two variables:
            - type which could be: art, artwork, artist
            - value: the variable with the change
    """
    message = "A new %s, %s, was successfully updated" % (type, value)
    print message
    flash(message)


def message_create(type, value):
    """
        Creates two messages respectively for the back (print) and the front end (flash())
        Gets two variables:
            - type which could be: art, artwork, artist
            - value: the variable with the change
    """

    message = "The %s, %s, was successfully created" % (type, value)
    print message
    flash(message)


def message_delete(type, value):
    """
        Creates two messages respectively for the back (print) and the front end (flash())
        Gets two variables:
            - type which could be: art, artwork, artist
            - value: the variable with the change
    """
    message = "The %s, %s, and its child dependencies -if existing- were successfully deleted" % (
        type, value)
    print message
    flash(message)


def message_failed_login():
    """
        sends a flash message
    """
    message = "Sorry, the login failed. Please try again" 
    flash(message)


def getList(input):
    output = input.replace('[', '')
    output = output.replace(']', '')
    output = output.replace(' ', '')

    return output.split(',')


def getUserID(email):
    try:
        retrieved_user = session.query(User).filter_by(email = email).one()
        return retrieved_user.id

    except:
        return None


def createUser(login_session):
    newUser = User(name = login_session['username'],
                   email = login_session['email'])

    session.add(newUser)
    session.commit()

    retrieved_user = session.query(User).filter_by(email = login_session['email']).one()
    return retrieved_user.id


def checkLogin():
    """ 
        This function which checks whether 
            - the user is logged in -> returning True
            - no user is logged in  -> returning False   
    """
    try:
        if login_session['user_id'] != None:
            print "login granted"
            return True
        else:
            print "login failed (error 1)"
            message = "Sorry, you lack the permission to do such an action. Please log in"
            flash(message)
            return False
    except:
        print "login failed (error 2)"
        message = "Sorry, you lack the permission to do such an action. Please log in"
        flash(message)
        return False


def checkUser(Class, id):
    """
        This function search whether the user is allowed to modified an entry
    """

    author = session.query(Class).filter_by(id = id).one().user_id

    # user_id = 1 is the admin which was created by the database population
    if login_session['user_id'] == 1:
        message = "You're logged in as admin, aka godlike user. You can modify every entry"
        flash(message)
        return True

    # for training purpose, a logged in user can modify an entry done by the admin
    # would be deleted later on.
    elif ((login_session['user_id'] == author) or (author == 1)):
        return True

    else: 
        message = "This post was created by another user. You can't modify it" 
        flash(message)
        return False


"""
    VI. Webserver
"""
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
