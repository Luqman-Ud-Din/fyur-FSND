from flask import render_template, request, flash, redirect, url_for

from config import app, db
from forms import VenueForm
from models import Venue


@app.route('/venues')
def venues():
    data = []
    locations = Venue.query.with_entities(Venue.city, Venue.state).distinct().all()
    for city, state in locations:
        d = {
            'city': city,
            'state': state,
            'venues': [v.serialize() for v in Venue.query.filter_by(city=city, state=state).all()]
        }
        data.append(d)

    return render_template('pages/venues.html', areas=data);


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term') or ''
    venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%'))

    response = {
        'count': venues.count(),
        'data': [venue.serialize() for venue in venues.all()]
    }

    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    data = Venue.query.filter_by(id=venue_id).first()

    if data:
        data.genres = (data.genres or '').split(',')

    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    try:
        request_data = {**request.form}
        request_data['genres'] = ','.join(request.form.getlist('genres') or [])
        request_data['seeking_talent'] = (request_data.get('seeking_talent') or '').lower() == 'y'
        venue = Venue(**request_data)
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        flash('Venue ' + request.form['name'] + ' was failed!')
        db.session.rollback()
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.filter_by(id=venue_id).first()

    if venue:
        venue = venue.serialize()
        venue['genres'] = venue['genres'].split(',')

    form = VenueForm(**(venue or {}))

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    try:
        request_data = {**request.form}
        request_data['genres'] = ','.join(request.form.getlist('genres') or [])
        request_data['seeking_talent'] = (request_data.get('seeking_talent') or '').lower() == 'y'
        Venue.query.filter_by(id=venue_id).update(request_data)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully updated!')
    except:
        flash('Venue ' + request.form['name'] + ' was not updated!')
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))
