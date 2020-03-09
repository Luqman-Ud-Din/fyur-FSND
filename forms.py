from datetime import datetime

from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, URL, Optional

from constants import State, Genre
from validators import ValidatePattern


class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )


class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=State.choices()
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=Genre.choices()
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website = StringField(
        'website', validators=[URL()]
    )

    seeking_talent = BooleanField('seeking_talent')

    seeking_description = StringField('seeking_description')


class ArtistForm(Form):
    name = StringField(
        'Name',
        validators=[DataRequired()]
    )
    city = StringField(
        'City',
        validators=[DataRequired()]
    )
    state = SelectField(
        'State',
        validators=[DataRequired()],
        choices=State.choices()
    )
    phone = StringField(
        'Phone',
        validators=[ValidatePattern(pattern=r'^\d{3}-\d{3}-\d{4}$')],
    )
    image_link = StringField(
        'Image Link',
        validators=[Optional(), URL()]
    )
    genres = SelectMultipleField(
        'Genres',
        validators=[DataRequired()],
        choices=Genre.choices()
    )
    facebook_link = StringField(
        'Facebook Link',
        validators=[Optional(), URL()]
    )
    website = StringField(
        'Website', validators=[Optional(), URL()]
    )
    seeking_venue = BooleanField('Seeking Venue')
    seeking_description = StringField('Seeking Description')
