from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# -------------------------------------------------------------------------- #
# Models.
# -------------------------------------------------------------------------- #


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String)
    seeking_talent = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable=False)
    genres = db.Column(db.ARRAY(db.String))

    shows = db.relationship('Show', backref='venue', lazy=True)


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String)
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable=False)
    genres = db.Column(db.ARRAY(db.String))

    shows = db.relationship('Show', backref='artist', lazy=True)


class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    venue_id = db.Column(
      db.Integer,
      db.ForeignKey('venues.id'),
      nullable=False,
    )
    artist_id = db.Column(
      db.Integer,
      db.ForeignKey('artists.id'),
      nullable=False,
    )
