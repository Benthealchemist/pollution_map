from flask import render_template, flash, redirect
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user, login_required
from app.forms import PostForm
from app.models import Post


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Great job submitting that post, Hun!')
        return redirect('/index')

    posts = current_user.posts.all()
    return render_template('index.html', title='Flask Yo.', user=user, posts=posts, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            #return redirect(url_for('login')) <- issue with redirect(url_for..)
            return redirect ('/login')
            flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        login_user(user, remember=form.remember_me.data)
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

#This renders the registration form, check in terminal whether users are being added to the db
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrats on signing your life away!')
        #return redirect(url_for('login')) <- issue with redirect(url_for..)
        return redirect ('/login')
    return render_template('register.html', title='Register', form=form)
    #something wrong with the url_for('login' action)



@app.route('/maps')
def maps():

    return render_template('maps.html', title ='Heat Maps')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/index')


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author':user, 'body':'Test post #1'},
        {'author':user, 'body':'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

# @app.route('/graphs')
# def graphs():
#     return render_template('graphs.html', title ='Graphs')
