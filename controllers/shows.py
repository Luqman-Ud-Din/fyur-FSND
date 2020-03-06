from flask import render_template, request, flash

from config import app, db
from forms import ShowForm
from models import Show


@app.route('/shows')
def shows():
    data = [show.serialize() for show in Show.query.all()]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    try:
        show = Show(**request.form)
        db.session.add(show)
        db.session.commit()
        flash(f'Show was successfully listed.')
    except Exception as ex:
        db.session.rollback()
        print(ex)
        flash(f'Show couldn\'t be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html')
