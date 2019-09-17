"""
  This file contains all the database connection definition,
  and all the CRUD for Fyyur web app.
"""
from sqlalchemy import Column, String, Integer, Boolean
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI
from flask_migrate import Migrate

DATABASE_PATH = SQLALCHEMY_DATABASE_URI

# print(DATABASE_PATH)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=DATABASE_PATH):
    """ Database setup """
    # print(database_path)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.app = app
    migrate = Migrate(app, db)
    db.init_app(app)
    db.create_all()

# All necessary CRUD operations superclass
class crud_ops():

    def insert(self):
        """ Insert data into venues table """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """ Update venue on venues table """
        db.session.commit()

    def delete(self):
        """ Delete venue on venues table """
        db.session.delete(self)
        db.session.commit()

# Defining Venue model
# Inherits from db.Model and crud_ops
class Venue(db.Model, crud_ops):
    __tablename__ = 'venue'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String(120))
    state = Column(String(120))
    address = Column(String(120))
    phone = Column(String(120))
    image_link = Column(String(500))
    facebook_link = Column(String(120))
    website = Column(String(250))
    seeking_talent = Column(Boolean, default=True)
    seeking_description = Column(String(500))

    def __init__(self, venue_id, name, city, state, address, phone,
                 image_link, facebook_link, website, seeking_talent,
                 seeking_description):
        self.website = website
        self.seeking_talent = seeking_talent
        self.seeking_description = seeking_description
        self.state = state
        self.address = address
        self.phone = phone
        self.image_link = image_link
        self.facebook_link = facebook_link
        self.city = city
        self.name = name
        self.id = venue_id

    def serialize(self):
        """ Serialize venue row """
        return {
            "website": self.website,
            "seeking_talent": self.seeking_talent,
            "seeking_description": self.seeking_description,
            "state": self.state,
            "address": self.address,
            "phone": self.phone,
            "image_link": self.image_link,
            "facebook_link": self.facebook_link,
            "city": self.city,
            "name": self.name,
            "id": self.id
        }


class Artist(db.Model, crud_ops):
    __tablename__ = 'artist'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String(120))
    state = Column(String(120))
    phone = Column(String(120))
    genres = Column(String(120))
    image_link = Column(String(500))
    facebook_link = Column(String(120))
    website = Column(String(250))
    seeking_venue = Column(Boolean, default=True)
    seeking_description = Column(String(500))

    def __init__(self, artist_id, name, city, state, phone, genres,
                 image_link, facebook_link, website, seeking_venue,
                 seeking_description):
        self.website = website
        self.seeking_venue = seeking_venue
        self.seeking_description = seeking_description
        self.city = city
        self.state = state
        self.phone = phone
        self.genres = genres
        self.image_link = image_link
        self.facebook_link = facebook_link
        self.name = name
        self.id = artist_id

    def serialize(self):
        """ Serialize venue row """
        return {
            "website": self.website,
            "seeking_venue": self.seeking_venue,
            "seeking_description": self.seeking_description,
            "state": self.state,
            "address": self.address,
            "genres": self.genres,
            "image_link": self.image_link,
            "facebook_link": self.facebook_link,
            "city": self.city,
            "name": self.name,
            "id": self.id
        }
