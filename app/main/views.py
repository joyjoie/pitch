from flask import render_template, request, redirect, url_for, abort
from . import main
from ..models import User, Pitch,Feedback
from .forms import PitchForm,FeedbackForm,UpdateProfile
from .. import db,photos
from flask_login import login_user, logout_user, login_required, current_user
import datetime


# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Welcome to Pitch'
    form = PitchForm()
    return render_template('index.html', form = form, title=title)
    

@main.route('/new_pitch', methods = ['GET','POST'])
@login_required
def new_pitch():
    form = PitchForm()

    if form.validate_on_submit():
        title = form.title.data
        pitch = Pitch(title=form.title.data)
        pitch.save_pitch()
        return redirect(url_for('main.index'))
    return render_template('new_pitch.html',form=form)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/new_feedback', methods = ['GET','POST'])
@login_required
def new_feedback():
    form = FeedbackForm()
    pitch = Pitch.query.get(id)
    if form.validate_on_submit():

        feedback = Feedback(title=form.title.data,feedback=form.feedback.data, pitch=pitch)
        db.session.add(feedback)
        db.session.commit()

    feed_back = Feedback.query.filter_by(pitch=pitch).all()
    return render_template('new_feedback.html',feed_back=feed_back,form=form)