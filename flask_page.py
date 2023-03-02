from flask import Flask, render_template, flash, url_for, redirect, jsonify
from forms import regForm, loginForm, twitterForm
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
import snscrape.modules.twitter as sntwitter
import re




app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Scp2859#@localhost/users'

db = SQLAlchemy(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def tweetRetrieval():
    form = twitterForm()
    query = "(from:" + form.twitter_username.data + ")"
    limit = 10
    count=0
    # tweet_user = ""
    # tweet_date = 0
    # tweet_content = ""
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        if count == limit:
            break
        else:
            # tweet_user = tweet.user.username
            # tweet_date = tweet.date
            # tweet_content = tweet.content
            tweetVar = Tweets(date=tweet.date, twitter_username=tweet.user.username, content=tweet.content)
            db.session.add(tweetVar)
            db.session.commit()
            flash('The tweets have been retrieved', 'Success')
    



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
class Tweets(db.Model):
    prim_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    twitter_username = db.Column(db.String(30))
    content = db.Column(db.String(1000))

    def __repr__(self):
        return f"Tweets('{self.date}', '{self.twitter_username}', '{self.content}')"   

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/register", endpoint="Register_page", methods=['GET', 'POST'])
def register():
    form = regForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You are now able to login', 'success')
        return redirect(url_for('login_page')) 
    return render_template('register.html', form=form)


@app.route("/login", endpoint="login_page", methods=['GET', 'POST'])
def login():
    form = loginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else: 
            flash('Login unsuccessful. Please check email or password', 'danger') 
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/twitter", endpoint="twitter", methods=['GET', 'POST'])
def tweetRetrieval():
    form = twitterForm()
    if form.validate_on_submit():
        query = "(from:" + form.twitter_username.data + ")"
        limit = 10
        count = 0
        for tweet in sntwitter.TwitterSearchScraper(query).get_items():
            count += 1
            if count == limit:
                break
            else:
                clean_content = re.sub(r'[^\x00-\x7F]+', '', tweet.rawContent)
                tweetVar = Tweets(date=tweet.date, twitter_username=tweet.user.username, content=clean_content)
                db.session.add(tweetVar)
                db.session.commit()
        display = Tweets.query.filter_by(twitter_username=form.twitter_username.data).first()
        flash('The tweets have been retrieved', 'Success')
    else:
        display = None
    return render_template('user_tweets.html', form=form, display=display)



if __name__ == '__main__':
    app.run(debug=True) 


