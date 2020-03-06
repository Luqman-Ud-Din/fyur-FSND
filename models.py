from datetime import datetime

from config import db

DATETIME_FORMAT = '%b %d %Y %H:%M:%S'


class BaseModel(db.Model):
    __abstract__ = True

    def serialize(self, detail=True):
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())


class Venue(BaseModel):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.Text, nullable=True)

    shows = db.relationship('Show', backref='venue', lazy=True)

    def __repr__(self):
        return f'<Venue {self.id} {self.name}>'

    @property
    def past_shows(self):
        return [{
            'artist_id': show.artist.id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': show.start_time.strftime(DATETIME_FORMAT)
        } for show in Show.query.filter(Show.start_time < datetime.now(), Show.venue_id == self.id).all()]

    @property
    def upcoming_shows(self):
        return [{
            'artist_id': show.artist.id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': show.start_time.strftime(DATETIME_FORMAT)
        } for show in Show.query.filter(Show.start_time >= datetime.now(), Show.venue_id == self.id).all()]

    def serialize(self, detail=True):
        venue = super().serialize(detail=detail)

        if detail:
            past_shows = self.past_shows
            upcoming_shows = self.upcoming_shows

            venue.update(
                {
                    'past_shows': past_shows,
                    'past_shows_count': len(past_shows),
                    'upcoming_shows': upcoming_shows,
                    'upcoming_shows_count': len(upcoming_shows),
                }
            )

        return venue


class Artist(BaseModel):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.Text, nullable=True)

    shows = db.relationship('Show', backref='artist', lazy=True)

    def __repr__(self):
        return f'<Artist {self.id} {self.name}>'

    @property
    def past_shows(self):
        return [{
            'venue_id': show.venue.id,
            'venue_name': show.venue.name,
            'venue_image_link': show.venue.image_link,
            'start_time': show.start_time.strftime(DATETIME_FORMAT)
        } for show in Show.query.filter(Show.start_time < datetime.now(), Show.artist_id == self.id).all()]

    @property
    def upcoming_shows(self):
        return [{
            'venue_id': show.venue.id,
            'venue_name': show.venue.name,
            'venue_image_link': show.venue.image_link,
            'start_time': show.start_time.strftime(DATETIME_FORMAT)
        } for show in Show.query.filter(Show.start_time >= datetime.now(), Show.artist_id == self.id).all()]

    def serialize(self, detail=True):
        artist = super().serialize(detail=detail)

        if detail:
            past_shows = self.past_shows
            upcoming_shows = self.upcoming_shows

            artist.update(
                {
                    'past_shows': past_shows,
                    'past_shows_count': len(past_shows),
                    'upcoming_shows': upcoming_shows,
                    'upcoming_shows_count': len(upcoming_shows),
                }
            )

        return artist


class Show(BaseModel):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)

    def __repr__(self):
        return f'<Show {self.id} {str(self.start_time)}>'

    def serialize(self, detail=True):
        show = super().serialize()

        if detail:
            show.update(
                {
                    "venue_name": self.venue.name,
                    "artist_name": self.artist.name,
                    "artist_image_link": self.artist.image_link
                }
            )

        show['start_time'] = self.start_time.strftime(DATETIME_FORMAT)

        return show
