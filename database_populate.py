"""
    Database_populate.py

    * programmed by Guillaume Simler
    * populate the database with a potential backbone 


"""

"""
    I. Import & Initialization
"""

# 1. Import modules

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Art, Artist, Artwork, Picture, User 
from security import escape

# 2. Connect to Database and create database session

engine = create_engine('sqlite:///artcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

"""
    II. Database population
"""
print
print "Starting Database population..."
print

# 1. Initial User

user = {"name" : "admin", "email" : "admin@myartcatalog.com"}


check_user = session.query(User).filter_by(name = user['name']).all()

if check_user: 
    print "The user %s is already in the database." % user['name']
    print "Please check your input and use the front end" 
else:
    
    insert_user = User(name= escape(user['name']), email= escape(user['email']))
    session.add(insert_user)
    print "The user %s will be added to the database" %user['name']

print "Committing..."
session.commit()

print 
print
print "Users committed"
print 
print
# 2. Art

arts = [{'type': 'Bronze', 
        'description': 'A classic material used by mankind since the age of the same name. This is by far the most popular cast metal sculpture types'},
        {'type': 'Painting',
         'description': 'The classic collection piece: painting is the application  of paint, pigments on a surface. This has been the major discipline in arts'}]


for art in arts:

    check_art = session.query(Art).filter_by(type = art['type']).all()

    if check_art: 
        print "The art (discipline) %s is already in the database." % art['type']
        print "Please check your input and use the front end" 
    else:
        insert_art = Art(type = escape(art['type']), 
                         description= escape(art['description']),
                         user_id = 1)
        session.add(insert_art)
        print "The art (discipline) %s will be added to the database" %art['type']

print "Committing..."
session.commit()
print 
print
print "Arts committed"
print 
print


# 3. Artist

artists = [{'name'         : 'Elke Zimmermann',
            'information'  : 'Elke is German contemporary sculptor, living and working in Moersach. I discovered her at an exhibition at Schillingfuerst in 2011. Elke mostly but not exclusivelly creates animal sculptures. Her husband, Reinhard, is a painter of his own right.',
            'url'          : 'http://www.atelier-zimmermann.de/',
            'user_id'      : 1},

           {'name'         : 'Hendrick Bobock',
            'information'  : "Hendrick Bobock is a German painter who had quite an active presence on ebay in the early 2000's before being 'washed out' by Chinese painters. His expressive paintings were at a very interesting price which made them suitable for temporary presentation. Yet a decade later, they weren't the ones sorted out.",
            'url'          : 'https://www.xing.com/profile/Hendrik_Bobock',
            'user_id'      : 1},

           {'name'         : 'Python',
            'information'  : "Python was quite the start in Nantes' epicier des arts, a non-profit and often bankrupt gallery. Pyhton was an art student at the academy. Unfortunately he suffered from psychotic breaks: either he was seddated and could not paint or was off the meds, could paint but was a danger to himself and others. His pictures reflect his medical condition as well as the influence of his studies at that time (e.g. Egon Schiele)",
            'url'          : '',
            'user_id'      : 1},

           {'name'         : 'Alexandre Ouline',
            'information'  : "The Belgian sculptor (1918-1940) worked in the classic Art Deco period, the second important period of modern bronze cast scultpures.",
            'url'          : '',
            'user_id'      : 1},
            ]

for artist in artists:

    check_artist = session.query(Artist).filter_by(name = artist['name']).first()

    if check_artist: 
        print "This artist %s seems to be already in the database." % artist['name']
        print "Please check your input and use the front end" 
    else:
        insert_artist= Artist(name = escape(artist['name']), 
                             information= escape(artist['information']),
                             url = escape(artist['url']),
                             user_id = artist['user_id']
                             )
        session.add(insert_artist)
        print "The artist %s will be added to the database" % artist['name']

print "Committing..."
session.commit()
print 
print
print "Artists committed"
print 
print
# 4. Artwork

artworks = [{'name'        : 'Albatros sur une vague',
            'description'  : 'Albatross on his wave, quite a usual Artdeco motive, with green patina',
            'purchase_year': '1989',
            'size'         : '',
            'weight'       : '17 kg',
            'user_id'      : 1,
            'art_id'       : 1,
            'artist_id'    : 4},

           {'name'         : 'Cachalot/Potwal',
            'description'  : 'Unusual motive as aquatic animals are quite difficult to dispict (they are not bound to gravity to stand, the scultpure would need it). Commissioned piece',
            'purchase_year': '2014',
            'size'         : '',
            'weight'       : '',
            'user_id'      : 1,
            'art_id'       : 1,
            'artist_id'    : 1},

            {'name'        : 'Dromedary',
            'description'  : "Looks like a old standard by Duke Ellington sounds,  majestic, smooth, in black patina. Was exhibited in Elke's yard",
            'purchase_year': '2012',
            'size'         : '',
            'weight'       : '',
            'user_id'      : 1,
            'art_id'       : 1,
            'artist_id'    : 1},

            {'name'        : 'Rhinoceros',
            'description'  : "Powerful, calm. It's a second cast (the first being owned by the artist's husband), black patina (applied after the purchase)",
            'purchase_year': '2011',
            'size'         : 'n.a.',
            'weight'       : 'n.a.',
            'user_id'      : 1,
            'art_id'       : 1,
            'artist_id'    : 1},

            {'name'        : 'no title Egon Shiele',
            'description'  : "A present by my parents, knowing my love for Egon Schiele, which must have been studied by the author at that time",
            'purchase_year': '2008',
            'size'         : 'n.a.',
            'weight'       : 'n.a.',
            'user_id'      : 1,
            'art_id'       : 2,
            'artist_id'    : 3},

            {'name'        : 'no title family fight',
            'description'  : "The purchase of this painting nearly ended in a family fight as my father and I dearly wanted it. My mother arbitrated in my favour. Yet it needs to remain in my office which prompts my father to offer it 'asylum'",
            'purchase_year': '2010',
            'size'         : '',
            'weight'       : '',
            'user_id'      : 1,
            'art_id'       : 2,
            'artist_id'    : 3},

            {'name'        : 'Queen Mary II',
            'description'  : "A present by my parents for my flat in Nantes, the namesake had left the drydocks of St Nazaire 2 years before",
            'purchase_year': '2006',
            'size'         : '',
            'weight'       : '',
            'user_id'      : 1,
            'art_id'       : 2,
            'artist_id'    : 2},

            {'name'        : 'Sun',
            'description'  : "One early picture I purchased, works well in pair with 'Window (red)'",
            'purchase_year': '1998',
            'size'         : '',
            'weight'       : '',
            'user_id'      : 1,
            'art_id'       : 2,
            'artist_id'    : 2},

            {'name'        : 'no title small yellow head',
            'description'  : "A present by my sister",
            'purchase_year': '2008',
            'size'         : '',
            'weight'       : '',
            'user_id'      : 1,
            'art_id'       : 2,
            'artist_id'    : 3},

            {'name'        : 'no title woman in red',
            'description'  : "A present by my sister",
            'purchase_year': '2010',
            'size'         : '',
            'weight'       : '',
            'user_id'      : 1,
            'art_id'       : 2,
            'artist_id'    : 3},

            {'name'        : 'Windows red',
            'description'  : "One early picture I purchased, works well in pair with 'Sun'",
            'purchase_year': '1998',
            'size'         : '',
            'weight'       : '',
            'user_id'      : 1,
            'art_id'       : 2,
            'artist_id'    : 2},

            {'name'        : 'Japanase blue dyptic',
            'description'  : "A dyptic from Hendrick Bobock. Refreshing, simple always a candidate to be kickout. Yet still on the walls",
            'purchase_year': '1999',
            'size'         : '',
            'weight'       : '',
            'user_id'      : 1,
            'art_id'       : 2,
            'artist_id'    : 2}
           ]

for artwork in artworks:

    with session.no_autoflush:
        check_artwork = session.query(Artwork).filter_by(name = artwork['name']).first()

    if check_artwork: 
        print "This artwork %s seems to be already in the database." % artwork['name']
        print "Please check your input and use the front end" 
        print
    else:
        insert_artwork= Artwork(name = escape(artwork['name']), 
                             description= escape(artwork['description']),
                             purchase_year = escape(artwork['purchase_year']),
                             size = escape(artwork['size']),
                             weight = escape(artwork['weight']),
                             user_id = artwork['user_id'],
                             art_id = artwork['art_id'],
                             artist_id = artwork['artist_id']
                             )
        session.add(insert_artwork)
        session.commit()
        print "The artworks %s will be added to the database" % artwork['name']
        print


print "Committing..."
session.commit()
print 
print "!!!!!!!!!!!!!!!!!!"
print "Artworks committed"
print "!!!!!!!!!!!!!!!!!!"
print
# 5. Pictures

pictures = [
            {'filename'     : '1-1.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '1'},

            {'filename'     : '1-2.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '1'},

            {'filename'     : '1-3.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '1'},

            {'filename'     : '1-4.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '1'},

            {'filename'     : '1-5.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '1'},

            {'filename'     : '3-1.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '3'},

            {'filename'     : '3-2.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '3'},

            {'filename'     : '3-3.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '3'},

            {'filename'     : '3-4.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '3'},

            {'filename'     : '3-5.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '3'},

            {'filename'     : '3-6.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '3'},

            {'filename'     : '4-1.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '4'},

            {'filename'     : '4-2.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '4'},

            {'filename'     : '4-3.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '4'},

            {'filename'     : '4-4.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '4'},

            {'filename'     : '4-5.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '4'},

            {'filename'     : '4-6.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '4'},

            {'filename'     : '5-1.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '5'},

            {'filename'     : '6-1.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '6'},

            {'filename'     : '7-1.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '7'},

            {'filename'     : '8-1.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '8'},

            {'filename'     : '9-1.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '9'},

            {'filename'     : '10-1.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '10'},

            {'filename'     : '11-1.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '11'},

            {'filename'     : '12-1.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '12'},

            {'filename'     : '12-2.jpg',
             'photographer' : 'Andre Wirsig',
             'artwork_id'   : '12'}]

for picture in pictures:
    
    check_picture = session.query(Picture).filter_by(filename = picture['filename']).first()

    if check_picture: 
        print "This file, %s, seems to be already in the database." % picture['filename']
        print "Please check your input and use the front end" 
    else:
        insert_picture= Picture(filename = picture['filename'],
                                photographer = picture['photographer'],
                                artwork_id = picture['artwork_id']
                             )
        session.add(insert_picture)
        print "The file, %s, will be added to the database" % picture['filename']


print "Committing..."
session.commit()
print "Imports committed"
print

