from flask import render_template, request, flash, redirect, url_for

from config import app, db
from forms import ArtistForm
from models import Artist


@app.route('/artists')
def artists():
    data = Artist.query.with_entities(Artist.id, Artist.name).all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term') or ''
    artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%'))

    response = {
        'count': artists.count(),
        'data': [artist.serialize() for artist in artists.all()]
    }

    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.filter_by(id=artist_id).first()

    if artist:
        artist = artist.serialize()
        artist['genres'] = (artist['genres'] or '').split(',')

    return render_template('pages/show_artist.html', artist=artist)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.filter_by(id=artist_id).first()

    if artist:
        artist = artist.serialize()
        artist['genres'] = artist['genres'].split(',')

    form = ArtistForm(**(artist or {}))

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    try:
        request_data = {**request.form}
        request_data['genres'] = ','.join(request.form.getlist('genres') or [])
        request_data['seeking_venue'] = (request_data.get('seeking_venue') or '').lower() == 'y'
        Artist.query.filter_by(id=artist_id).update(request_data)
        db.session.commit()
        flash(f'Artist {request.form["name"]} was successfully updated!')
    except:
        flash(f'Artist {request.form["name"]} was not updated!')
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    try:
        request_data = {**request.form}
        request_data['genres'] = ','.join(request.form.getlist('genres') or [])
        request_data['seeking_venue'] = (request_data.get('seeking_venue') or '').lower() == 'y'
        artist = Artist(**request_data)
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        flash('Artist ' + request.form['name'] + ' was failed!')
        db.session.rollback()
    finally:
        db.session.close()

    return render_template('pages/home.html')
