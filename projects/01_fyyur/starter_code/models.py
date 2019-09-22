"""
  This file contains all the database connection definition,
  and all the CRUD for Fyyur web app.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate

DATABASE_PATH = Config.SQLALCHEMY_DATABASE_URI


db = SQLAlchemy()


def setup_db(app, database_path=DATABASE_PATH):
    """ Database setup """
    # print(database_path)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.app = app
    migrate = Migrate(app, db)
    db.init_app(app)
    # No need to run db.create_all() as for now using flask migrations
    # library.
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


class Link(db.Model, crud_ops):
    __tablename__="link"
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.id"), primary_key=True)
    likes = db.Column(db.Integer)
    deslikes = db.Column(db.Integer)


class Genre(db.Model, crud_ops):
    __tablename__ = "genres"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(250))
    artists = db.relationship("Artist", secondary="link")

    def __init__(self, genre_id, name, description, artists):
        self.id = genre_id
        self.name = name
        self.description = description
        self.artists = artists

    def serialize(self):
        """ Serialize genres table row data """
        return {
            "genre_id": self.genre_id,
            "name": self.name,
            "description": self.description
        }

# Defining Venue model
# Inherits from db.Model and crud_ops
class Venue(db.Model, crud_ops):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(250))
    seeking_talent = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship("Show")
    address = db.relationship("Venue_Address")

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
        """ Serialize venues table row data """
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


class Venue_Address(db.Model, crud_ops):
    __tablename__ = "venue_address"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(250))
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), nullable=False)
    venue = db.relationship(Venue, back_populates="addresses")


class Artist(db.Model, crud_ops):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    instagram_link = db.Column(db.String(120))
    website = db.Column(db.String(250))
    seeking_venue = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String(500))
    genres = db.relationship(Genre, secondary="link")
    shows = db.relationship("Show")

    def __init__(self, artist_id, name, city, state, phone,
                 image_link, facebook_link, website, seeking_venue,
                 seeking_description, genres):
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
        """ Serialize artists table row data """
        return {
            "website": self.website,
            "seeking_venue": self.seeking_venue,
            "seeking_description": self.seeking_description,
            "state": self.state,
            "genres": self.genres,
            "image_link": self.image_link,
            "facebook_link": self.facebook_link,
            "city": self.city,
            "name": self.name,
            "id": self.id
        }


class Show(db.Model, crud_ops):
    __tablename__ = "shows"

    artist = db.relationship(Artist, back_populates="shows")
    venue = db.relationship(Venue, back_populates="shows")
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id"), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.now())
    ticket_price = db.Column(db.String(15))

    def __init__(self, show_id, artist_id, venue_id, start_time, ticket_price):
        self.id = show_id
        self.venue_id = venue_id
        self.artist_id = artist_id
        self.start_time = start_time
        self.ticket_price = ticket_price

    def serialize(self):
        """ Serialize Shows table row data """
        return {
            "show_id": self.id,
            "venue_id": self.venue_id,
            "artist_id": self.artist_id,
            "start_time": self.start_time,
            "ticket_price": self.ticket_price
        }
