""" This is the base folder for Udacity the Fyyr project app """
# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import babel
import dateutil.parser
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_moment import Moment
from forms import *
from models import *
from flask_cors import CORS

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

# app = Flask(__name__)
# app.config.from_object('config')
# setup_db(app)
# db = SQLAlchemy(app)

# @@TODO: connect to a local postgresql database
# Done in config.py file
# s = datetime.strftime(show.start_time, "%Y-%m-%d %H:%M")
# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

# @TODO Implement Show and Artist models,
# and complete all model relationships and properties,
# as a database migration.
# Done in models.py file

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#
CURRENT_DATE = datetime.now()


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

def create_app(test_config=None):
    """ create and configure the app """
    app = Flask(__name__)
    setup_db(app)
    moment = Moment(app)
    CORS(app)
    app.jinja_env.filters['datetime'] = format_datetime

    # CORS Headers

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # @TODO: Define ERROR handlers functions

    @app.errorhandler(404)
    def not_found(error):
        """ Returns 404 not found Error """
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        """ Returns 400 Bad Request Error """
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(422)
    def unprocessable_entity(error):
        """ Returns 422 Unprocessable Request Error """
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Request"
        }), 422

    #  Venues
    @app.route('/')
    def index():
        return render_template('pages/home.html')

    #  ----------------------------------------------------------------

    @app.route('/venues')
    def venues():
        # @TODO: replace with real venues data.
        #   num_shows should be aggregated based on number of upcoming shows per venue.
        # Gathering data from database
        cities = City.query.all()
        data = [{"city": city.name,
                 "state": city.state,
                 "venues": [{"id": v_a.venues.id,
                             "name": v_a.venues.name,
                             "num_upcoming_shows":
                                 [v_s.artists for v_s in v_a.venues.shows
                                  if v_s.start_time > CURRENT_DATE]
                             }
                            for v_a in city.venues_address]
                 } for city in cities]
        # print(data)
        # print(venues)
        # data = [{
        #     "city": "San Francisco",
        #     "state": "CA",
        #     "venues": [{
        #         "id": 1,
        #         "name": "The Musical Hop",
        #         "num_upcoming_shows": 0,
        #     }, {
        #         "id": 3,
        #         "name": "Park Square Live Music & Coffee",
        #         "num_upcoming_shows": 1,
        #     }]
        # }, {
        #     "city": "New York",
        #     "state": "NY",
        #     "venues": [{
        #         "id": 2,
        #         "name": "The Dueling Pianos Bar",
        #         "num_upcoming_shows": 0,
        #     }]
        # }]
        return render_template('pages/venues.html', areas=data)

    @app.route('/venues/search', methods=['POST'])
    def search_venues():
        # @TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
        # seach for Hop should return "The Musical Hop".
        # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
        venue_hint = "%{}%".format(request.form.get("search_term"))
        search_result = Venue.query.filter(Venue.name.ilike(venue_hint)).all()
        # print(search_result[0])
        data = [{"id": venue.id,
                 "name": venue.name} for venue in search_result]
        # Returning the response object
        response = {
            "data": data,
            "count": len(search_result)
        }
        return render_template('pages/search_venues.html', results=response,
                               search_term=request.form.get('search_term', ''))


    @app.route('/venues/<int:venue_id>')
    def show_venue(venue_id):
        # shows the venue page with the given venue_id
        # @TODO: replace with real venue data from the venues table, using venue_id
        venue = Venue.query.filter(Venue.id == venue_id).one_or_none()
        # print(artist.shows)
        genres = [genre.name for genre in venue.genres]
        shows = [show for show in venue.shows]
        past_shows = [{"artist_id": show.artist_id,
                       "artist_name": show.artists.name,
                       "artist_image_link": show.artists.image_link,
                       "start_time": format_datetime(str(show.start_time), format="full")
                       } for show in shows
                      if show.start_time < CURRENT_DATE]
        upcoming_shows = [{"artist_id": show.artist_id,
                           "artist_name": show.artists.name,
                           "artist_image_link": show.artists.image_link,
                           "start_time": format_datetime(str(show.start_time), format="full")
                           } for show in shows
                          if show.start_time > CURRENT_DATE]
        # print(genres)
        data = {"id": venue.id,
                "name": venue.name,
                "genres": genres,
                "address": venue.venue_address[0].address,
                "city": venue.venue_address[0].cities[0].name,
                "state": venue.venue_address[0].cities[0].state,
                "phone": venue.venue_address[0].phone,
                "website": venue.website,
                "facebook_link": venue.facebook_link,
                "seeking_talent": venue.seeking_talent,
                "seeking_description": venue.seeking_description,
                "image_link": venue.image_link,
                "past_shows": past_shows,
                "upcoming_shows": upcoming_shows,
                "past_shows_count": len(past_shows),
                "upcoming_shows_count": len(upcoming_shows)
                }
        # data1 = {
        #     "id": 1,
        #     "name": "The Musical Hop",
        #     "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        #     "address": "1015 Folsom Street",
        #     "city": "San Francisco",
        #     "state": "CA",
        #     "phone": "123-123-1234",
        #     "website": "https://www.themusicalhop.com",
        #     "facebook_link": "https://www.facebook.com/TheMusicalHop",
        #     "seeking_talent": True,
        #     "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        #     "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
        #     "past_shows": [{
        #         "artist_id": 4,
        #         "artist_name": "Guns N Petals",
        #         "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        #         "start_time": "2019-05-21T21:30:00.000Z"
        #     }],
        #     "upcoming_shows": [],
        #     "past_shows_count": 1,
        #     "upcoming_shows_count": 0,
        # }
        # data2 = {
        #     "id": 2,
        #     "name": "The Dueling Pianos Bar",
        #     "genres": ["Classical", "R&B", "Hip-Hop"],
        #     "address": "335 Delancey Street",
        #     "city": "New York",
        #     "state": "NY",
        #     "phone": "914-003-1132",
        #     "website": "https://www.theduelingpianos.com",
        #     "facebook_link": "https://www.facebook.com/theduelingpianos",
        #     "seeking_talent": False,
        #     "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
        #     "past_shows": [],
        #     "upcoming_shows": [],
        #     "past_shows_count": 0,
        #     "upcoming_shows_count": 0,
        # }
        # data3 = {
        #     "id": 3,
        #     "name": "Park Square Live Music & Coffee",
        #     "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
        #     "address": "34 Whiskey Moore Ave",
        #     "city": "San Francisco",
        #     "state": "CA",
        #     "phone": "415-000-1234",
        #     "website": "https://www.parksquarelivemusicandcoffee.com",
        #     "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
        #     "seeking_talent": False,
        #     "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
        #     "past_shows": [{
        #         "artist_id": 5,
        #         "artist_name": "Matt Quevedo",
        #         "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        #         "start_time": "2019-06-15T23:00:00.000Z"
        #     }],
        #     "upcoming_shows": [{
        #         "artist_id": 6,
        #         "artist_name": "The Wild Sax Band",
        #         "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        #         "start_time": "2035-04-01T20:00:00.000Z"
        #     }, {
        #         "artist_id": 6,
        #         "artist_name": "The Wild Sax Band",
        #         "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        #         "start_time": "2035-04-08T20:00:00.000Z"
        #     }, {
        #         "artist_id": 6,
        #         "artist_name": "The Wild Sax Band",
        #         "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        #         "start_time": "2035-04-15T20:00:00.000Z"
        #     }],
        #     "past_shows_count": 1,
        #     "upcoming_shows_count": 1,
        # }
        # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
        return render_template('pages/show_venue.html', venue=data)

    #  Create Venue
    #  ----------------------------------------------------------------

    @app.route('/venues/create', methods=['GET'])
    def create_venue_form():
        form = VenueForm()
        return render_template('forms/new_venue.html', form=form)

    @app.route('/venues/create', methods=['POST'])
    def create_venue_submission():
        # @TODO: insert form data as a new Venue record in the db, instead
        # @TODO: modify data to be the data object returned from db insertion

        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
        # @TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        return render_template('pages/home.html')

    @app.route('/venues/<venue_id>', methods=['DELETE'])
    def delete_venue(venue_id):
        # @TODO: Complete this endpoint for taking a venue_id, and using
        # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

        # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
        # clicking that button delete it from the db then redirect the user to the homepage
        return None

    #  Artists
    #  ----------------------------------------------------------------
    @app.route('/artists')
    def artists():
        # @TODO: replace with real data returned from querying the database
        artist_list = Artist.query.all()
        serialized_artist_list = [artist.serialize() for artist in artist_list]
        # print(serialized_artist_list)
        data = [{"id": row["id"], "name": row["name"]} for row in serialized_artist_list]
        return render_template('pages/artists.html', artists=data)

    @app.route('/artists/search', methods=['POST'])
    def search_artists():
        # @TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
        # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
        # search for "band" should return "The Wild Sax Band".
        # Getting current data so that can compare it to the shows start time
        artist_hint = "%{}%".format(request.form.get("search_term"))
        search_result = Artist.query.filter(Artist.name.ilike(artist_hint)).all()
        # Since we can get more than one artist we only get the
        # number of upcoming shows if we get one artist instead of
        # a list of artists
        # If the search_result has more than one artist
        # upcoming_shows list will still empty
        # Else if the result is only one artist
        # Then the upcoming_shows list shall be fulfilled with the shows
        # print(search_result[0])
        data = [{"id": artist.id,
                 "name": artist.name} for artist in search_result]
        # Returning the response object
        response = {
            "data": data,
            "count": len(search_result)
        }

        return render_template('pages/search_artists.html', results=response,
                               search_term=request.form.get('search_term', ''))

    @app.route('/artists/<int:artist_id>')
    def show_artist(artist_id):
        # shows the artist page with the given artist_id
        # @TODO: replace with real artist data from the artists table, using artist_id
        artist = Artist.query.filter(Artist.id == artist_id).one_or_none()
        # print(artist.shows)
        genres = [genre.name for genre in artist.genres]
        shows = [show for show in artist.shows]
        past_shows = [{"venue_id": show.venue_id,
                       "venue_name": show.venues.name,
                       "venue_image_link": show.venues.image_link,
                       "start_time": format_datetime(str(show.start_time), format="full")
                       } for show in shows
                      if show.start_time < CURRENT_DATE]
        upcoming_shows = [{"venue_id": show.venue_id,
                           "venue_name": show.venues.name,
                           "venue_image_link": show.venues.image_link,
                           "start_time": format_datetime(str(show.start_time), format="full")
                           } for show in shows
                          if show.start_time > CURRENT_DATE]
        # print(genres)
        data = {"id": artist.id,
                "name": artist.name,
                "genres": genres,
                "city": artist.city,
                "state": artist.state,
                "phone": artist.phone,
                "website": artist.website,
                "facebook_link": artist.facebook_link,
                "seeking_venue": artist.seeking_venue,
                "seeking_description": artist.seeking_description,
                "image_link": artist.image_link,
                "past_shows": past_shows,
                "upcoming_shows": upcoming_shows,
                "past_shows_count": len(past_shows),
                "upcoming_shows_count": len(upcoming_shows)
                }
        """data1 = {
            "id": 2,
            "name": "Guns N Petals",
            "genres": ["Rock n Roll"],
            "city": "San Francisco",
            "state": "CA",
            "phone": "326-123-5000",
            "website": "https://www.gunsnpetalsband.com",
            "facebook_link": "https://www.facebook.com/GunsNPetals",
            "seeking_venue": True,
            "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
            "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
            "past_shows": [{
                "venue_id": 1,
                "venue_name": "The Musical Hop",
                "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
                "start_time": "2019-05-21T21:30:00.000Z"
            }],
            "upcoming_shows": [],
            "past_shows_count": 1,
            "upcoming_shows_count": 0,
        }
        data2 = {
            "id": 3,
            "name": "Matt Quevedo",
            "genres": ["Jazz"],
            "city": "New York",
            "state": "NY",
            "phone": "300-400-5000",
            "facebook_link": "https://www.facebook.com/mattquevedo923251523",
            "seeking_venue": False,
            "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
            "past_shows": [{
                "venue_id": 3,
                "venue_name": "Park Square Live Music & Coffee",
                "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
                "start_time": "2019-06-15T23:00:00.000Z"
            }],
            "upcoming_shows": [],
            "past_shows_count": 1,
            "upcoming_shows_count": 0,
        }
        data3 = {
            "id": 4,
            "name": "The Wild Sax Band",
            "genres": ["Jazz", "Classical"],
            "city": "San Francisco",
            "state": "CA",
            "phone": "432-325-5432",
            "seeking_venue": False,
            "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "past_shows": [],
            "upcoming_shows": [{
                "venue_id": 3,
                "venue_name": "Park Square Live Music & Coffee",
                "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
                "start_time": "2035-04-01T20:00:00.000Z"
            }, {
                "venue_id": 3,
                "venue_name": "Park Square Live Music & Coffee",
                "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
                "start_time": "2035-04-08T20:00:00.000Z"
            }, {
                "venue_id": 3,
                "venue_name": "Park Square Live Music & Coffee",
                "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
                "start_time": "2035-04-15T20:00:00.000Z"
            }],
            "past_shows_count": 0,
            "upcoming_shows_count": 3,
        }
        """
        # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
        return render_template('pages/show_artist.html', artist=data)

    #  Update
    #  ----------------------------------------------------------------
    @app.route('/artists/<int:artist_id>/edit', methods=['GET'])
    def edit_artist(artist_id):
        form = ArtistForm()
        artist = {
            "id": 4,
            "name": "Guns N Petals",
            "genres": ["Rock n Roll"],
            "city": "San Francisco",
            "state": "CA",
            "phone": "326-123-5000",
            "website": "https://www.gunsnpetalsband.com",
            "facebook_link": "https://www.facebook.com/GunsNPetals",
            "seeking_venue": True,
            "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
            "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
        }
        # @TODO: populate form with fields from artist with ID <artist_id>
        return render_template('forms/edit_artist.html', form=form, artist=artist)

    @app.route('/artists/<int:artist_id>/edit', methods=['POST'])
    def edit_artist_submission(artist_id):
        # @TODO: take values from the form submitted, and update existing
        # artist record with ID <artist_id> using the new attributes

        return redirect(url_for('show_artist', artist_id=artist_id))

    @app.route('/venues/<int:venue_id>/edit', methods=['GET'])
    def edit_venue(venue_id):
        form = VenueForm()
        venue = {
            "id": 1,
            "name": "The Musical Hop",
            "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
            "address": "1015 Folsom Street",
            "city": "San Francisco",
            "state": "CA",
            "phone": "123-123-1234",
            "website": "https://www.themusicalhop.com",
            "facebook_link": "https://www.facebook.com/TheMusicalHop",
            "seeking_talent": True,
            "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
            "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
        }
        # @TODO: populate form with values from venue with ID <venue_id>
        return render_template('forms/edit_venue.html', form=form, venue=venue)

    @app.route('/venues/<int:venue_id>/edit', methods=['POST'])
    def edit_venue_submission(venue_id):
        # @TODO: take values from the form submitted, and update existing
        # venue record with ID <venue_id> using the new attributes
        return redirect(url_for('show_venue', venue_id=venue_id))

    #  Create Artist
    #  ----------------------------------------------------------------

    @app.route('/artists/create', methods=['GET'])
    def create_artist_form():
        form = ArtistForm()
        return render_template('forms/new_artist.html', form=form)

    @app.route('/artists/create', methods=['POST'])
    def create_artist_submission():
        # called upon submitting the new artist listing form
        # @TODO: insert form data as a new Venue record in the db, instead
        # @TODO: modify data to be the data object returned from db insertion

        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
        # @TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
        return render_template('pages/home.html')

    #  Shows
    #  ----------------------------------------------------------------

    @app.route('/shows')
    def shows():
        # displays list of shows at /shows
        # @TODO: replace with real venues data.
        #       num_shows should be aggregated based on number of upcoming shows per venue.
        shows = Show.query.all()

        data = [{"venue_id": shows[i].venue_id,
                 "venue_name": shows[i].venues.name,
                 "artist_id": shows[i].artist_id,
                 "artist_name": shows[i].artists.name,
                 "artist_image_link": shows[i].artists.image_link,
                 "start_time": format_datetime(str(shows[i].start_time), format="full")} for i in range(len(shows))]

        return render_template('pages/shows.html', shows=data)

    @app.route('/shows/create')
    def create_shows():
        # renders form. do not touch.
        form = ShowForm()
        return render_template('forms/new_show.html', form=form)

    @app.route('/shows/create', methods=['POST'])
    def create_show_submission():
        # called to create new shows in the db, upon submitting new show listing form
        # @TODO: insert form data as a new Show record in the db, instead

        # on successful db insert, flash success
        flash('Show was successfully listed!')
        # @TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Show could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        return render_template('pages/home.html')

    return app
