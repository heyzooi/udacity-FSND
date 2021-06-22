from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# -------------------------------------------------------------------------- #
# Models.
# -------------------------------------------------------------------------- #

venues_genres = db.Table(
  'venues_genres',
  db.Column(
    'venue_id',
    db.Integer,
    db.ForeignKey('venues.id'),
    primary_key=True,
  ),
  db.Column(
    'genre_id',
    db.Integer,
    db.ForeignKey('genres.id'),
    primary_key=True
  ),
)

artists_genres = db.Table(
  'artists_genres',
  db.Column(
    'artist_id',
    db.Integer,
    db.ForeignKey('artists.id'),
    primary_key=True,
  ),
  db.Column(
    'genre_id',
    db.Integer,
    db.ForeignKey('genres.id'),
    primary_key=True,
  ),
)


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

    # TODO: implement any missing fields, as a database migration using
    # Flask-Migrate
    shows = db.relationship('Show', backref='venue', lazy=True)
    genres = db.relationship(
      'Genre',
      secondary=venues_genres,
      lazy='subquery',
      backref=db.backref('venues', lazy=True),
    )


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

    # FIXED: implement any missing fields, as a database migration using
    # Flask-Migrate
    shows = db.relationship('Show', backref='artist', lazy=True)
    genres = db.relationship(
      'Genre',
      secondary=artists_genres,
      lazy='subquery',
      backref=db.backref('artists', lazy=True),
    )

# FIXED Implement Show and Artist models, and complete all model relationships
# and properties, as a database migration.


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


class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
