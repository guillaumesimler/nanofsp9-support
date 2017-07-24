"""
    Database_setup.py

    * programmed by Guillaume Simler
    * sets up the database


"""

"""
    I. Import & Initialization
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
 
Base = declarative_base()

"""
    II. Table definition
"""

class User(Base):
    """
        Defines the user class/table, more in the README.md
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String(250))
    email = Column(String(100))
    # picture is a string, as it would be an Url to the picture
    picture = Column(String(250))

    # For safety reasons, no serialization

class Art(Base):
    """
        Defines the Art class/table, more in the README.md
    """
    __tablename__ = 'art'
   
    id = Column(Integer, primary_key=True)
    type = Column(String(80))
    description = Column(Text)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(User)

    # no user input here, as it is such big a change
    # that it should not been driven by a front-end user

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'type'             : self.type,
           'id'               : self.id,
           'description'      : self.description,
           'user_id'          : self.user_id
       }
 
class Artist(Base):
    """
        Defines the artist class/table, more in the README.md
    """
    __tablename__ = 'artist'


    name =Column(String(120), nullable = False)
    id = Column(Integer, primary_key = True)
    information = Column(Text)
    url = Column(String(80))

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(User)


    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
           'information'  : self.information,
           'url'          : self.url,
           'user_id'      : self.user_id,
        }

class Artwork(Base):
    """
        Defines the artist class/table, more in the README.md
    """
    __tablename__ = 'artwork'


    name = Column(String(120), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(Text)
    purchase_year = Column(String(4))
    size = Column(String(20))
    weight = Column(String(20))
    purchase_prize = Column(String(80))

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(User)

    art_id = Column(Integer, ForeignKey('art.id'), nullable=False)
    art = relationship(Art)

    artist_id = Column(Integer, ForeignKey('artist.id'), nullable=False)
    artist = relationship(Artist)


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'name'          : self.name,
           'id'            : self.id,
           'description'   : self.description,
           'purchase_year' : self.purchase_year,
           'size'          : self.size,
           'weight'        : self.weight,
           'purchase_prize': self.purchase_prize,
           'user_id'       : self.user_id,
           'art_id'        : self.art_id,
           'artist_id'     : self.artist_id,
        }

class Picture(Base):
    """
        Defines the picture class/table, more in the README.md
    """
    __tablename__ = 'picture'


    filename = Column(String(80), nullable = False)
    photographer = Column(String(200))
    id = Column(Integer, primary_key = True)
    
    artwork_id = Column(Integer, ForeignKey('artwork.id'), nullable=False)
    artwork = relationship(Artwork)


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'id'           : self.id,
           'filename'     : self.filename,
           'photographer' : self.photographer,
           'artwork_id'   : self.artwork_id,
        }

"""
    III. Database setup
"""
server_select = ""


engine = create_engine('postgresql://datauser:beau@localhost/artcatalog')

if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)
print "DB Setup Loading Server version"
server_select = "Server"

print "DB Setup local version"



print "Database was created"