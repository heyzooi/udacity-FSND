# -------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------- #

from enum import unique
import json
import dateutil.parser
import babel
from flask import (
  Flask,
  render_template,
  request,
  Response,
  flash,
  redirect,
  url_for,
)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler, error
from flask_wtf import FlaskForm
from sqlalchemy.orm import backref, lazyload
from forms import *
from flask_migrate import Migrate, migrate
from collections import namedtuple
from datetime import date
from models import (
    db,
    Venue,
    Show,
    Artist,
)
import sys
# -------------------------------------------------------------------------- #
# App Config.
# -------------------------------------------------------------------------- #

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)


# -------------------------------------------------------------------------- #
# Filters.
# -------------------------------------------------------------------------- #


def format_datetime(date, format='medium'):
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

# -------------------------------------------------------------------------- #
# Controllers.
# -------------------------------------------------------------------------- #


@app.route('/')
def index():
    venues = Venue.query.order_by(Venue.created_at.desc()).limit(10).all()
    artists = Artist.query.order_by(Artist.created_at.desc()).limit(10).all()
    return render_template('pages/home.html', venues=venues, artists=artists)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows
    #       per venue.
    # data=[{
    #   "city": "San Francisco",
    #   "state": "CA",
    #   "venues": [{
    #     "id": 1,
    #     "name": "The Musical Hop",
    #     "num_upcoming_shows": 0,
    #   }, {
    #     "id": 3,
    #     "name": "Park Square Live Music & Coffee",
    #     "num_upcoming_shows": 1,
    #   }]
    # }, {
    #   "city": "New York",
    #   "state": "NY",
    #   "venues": [{
    #     "id": 2,
    #     "name": "The Dueling Pianos Bar",
    #     "num_upcoming_shows": 0,
    #   }]
    # }]
    cities = Venue.query.with_entities(
        Venue.city,
        Venue.state,
    ).distinct().order_by(
        'state',
        'city',
    ).all()
    Data = namedtuple('Data', ['city', 'state', 'venues'])
    data = []
    for city in cities:
        data.append(Data(
            city=city[0],
            state=city[1],
            venues=Venue.query.filter_by(
                city=city[0]
            ).filter_by(
                state=city[1]
            ).order_by(Venue.name).all(),
        ))
    # data = Venue.query.order_by.all()
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    result = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
    Response = namedtuple('Response', ['count', 'data'])
    response = Response(
        count=len(result),
        data=result,
    )
    return render_template(
        'pages/search_venues.html',
        results=response,
        search_term=search_term
    )


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id

    data = Venue.query.get(venue_id)
    past_shows = db.session.query(Show).join(Venue).filter(
        Show.venue_id == venue_id
    ).filter(
        Show.start_time < date.today()
    ).order_by(Show.start_time.desc()).all()
    upcoming_shows = db.session.query(Show).join(Venue).filter(
        Show.venue_id == venue_id
    ).filter(
        Show.start_time >= date.today()
    ).order_by(Show.start_time.desc()).all()
    return render_template(
        'pages/show_venue.html',
        venue=data,
        past_shows=past_shows,
        past_shows_count=len(past_shows),
        upcoming_shows=upcoming_shows,
        upcoming_shows_count=len(upcoming_shows),
    )

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    form = VenueForm(request.form)
    try:
        venue = Venue()
        form.populate_obj(venue)
        if form.validate():
            db.session.add(venue)
            db.session.commit()

            # on successful db insert, flash success
            flash(f'Venue {venue.name} was successfully listed!')
            return render_template('pages/home.html')
        else:
            print(form.errors)
            flash(f'An error occurred.')
            db.session.rollback()
            return render_template('forms/new_venue.html', form=form)
    except Exception:
        # TODO: on unsuccessful db insert, flash an error instead.
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        print(sys.exc_info())
        flash(f'An error occurred.')
        db.session.rollback()
        return render_template('forms/new_venue.html', form=form)
    finally:
        db.session.close()


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit
    # could fail.
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page,
    # have it so that clicking that button delete it from the db then redirect
    # the user to the homepage
    return redirect(url_for('index'))


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    data = Artist.query.order_by(Artist.name).all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', '')
    result = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
    Response = namedtuple('Response', ['count', 'data'])
    response = Response(
        count=len(result),
        data=result,
    )
    return render_template(
        'pages/search_artists.html',
        results=response,
        search_term=search_term,
    )


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id

    data = Artist.query.get(artist_id)

    past_shows = db.session.query(Show).join(Artist).filter(
        Show.artist_id == artist_id
    ).filter(
        Show.start_time < date.today()
    ).order_by(Show.start_time.desc()).all()

    upcoming_shows = db.session.query(Show).join(Artist).filter(
        Show.artist_id == artist_id
    ).filter(
        Show.start_time >= date.today()
    ).order_by(Show.start_time.desc()).all()

    return render_template(
        'pages/show_artist.html',
        artist=data,
        past_shows=past_shows,
        past_shows_count=len(past_shows),
        upcoming_shows=upcoming_shows,
        upcoming_shows_count=len(upcoming_shows)
    )


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    form.state.default = artist.state
    form.genres.default = artist.genres
    form.process()
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    try:
        form.populate_obj(artist)
        if form.validate():
            db.session.commit()

            return redirect(url_for('show_artist', artist_id=artist_id))
        else:
            print(form.errors)
            db.session.rollback()
            return render_template(
                'forms/edit_artist.html',
                form=form,
                artist=artist,
            )
    except Exception:
        print(sys.exc_info())
        flash(f'An error occurred.')
        db.session.rollback()
        return render_template(
            'forms/edit_artist.html',
            form=form,
            artist=artist,
        )
    finally:
        db.session.close()


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    form.state.default = venue.state
    form.genres.default = venue.genres
    form.process()
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    form = VenueForm(request.form)
    venue = Venue.query.get(venue_id)
    try:
        form.populate_obj(venue)
        if form.validate():
            db.session.add(venue)
            db.session.commit()

            return redirect(url_for('show_venue', venue_id=venue_id))
        else:
            print(form.errors)
            flash(f'An error occurred.')
            db.session.rollback()
            return render_template('forms/new_venue.html', form=form)
    except Exception:
        # TODO: on unsuccessful db insert, flash an error instead.
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        print(sys.exc_info())
        flash(f'An error occurred.')
        db.session.rollback()
        return render_template('forms/new_venue.html', form=form)
    finally:
        db.session.close()


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    form = ArtistForm()
    try:
        artist = Artist()
        form.populate_obj(artist)
        if form.validate():
            db.session.add(artist)
            db.session.commit()

            flash(f'Artist {artist.name} was successfully listed!')
            return render_template('pages/home.html')
        else:
            print(form.errors)
            flash(f'An error occurred.')
            db.session.rollback()
            return render_template('forms/new_artist.html', form=form)
    except Exception:
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        print(sys.exc_info())
        flash(f'An error occurred.')
        db.session.rollback()
        return render_template('forms/new_artist.html', form=form)
    finally:
        db.session.close()


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows
    #       per venue.
    data = Show.query.order_by(Show.start_time.desc()).all()
    # Tuesday May, 21, 2019 at 9:30PM
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing
    # form
    # TODO: insert form data as a new Show record in the db, instead
    show = Show(
        start_time=request.form['start_time'],
        venue_id=request.form['venue_id'],
        artist_id=request.form['artist_id'],
    )
    db.session.add(show)
    db.session.commit()

    # on successful db insert, flash success
    flash('Show was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    fmt = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    file_handler.setFormatter(
        Formatter(fmt)
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# -------------------------------------------------------------------------- #
# Launch.
# -------------------------------------------------------------------------- #

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
