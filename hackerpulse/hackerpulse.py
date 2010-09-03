from flask import Flask, render_template, session, g, redirect, url_for
from flaskext.openid import OpenID

app = Flask(__name__)
oid = OpenID(app)

@app.before_request
def lookup_current_user():
    """ Called before each request, used to set the active user in this session """
    g.user = None
    if 'openid' in session:
        pass #pull the user object from DB

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/login/')
@oid.loginhandler
def login():
    if g.user is not None:
        #user already logged in, redirect them
        return redirect(oid.get_next_url())
    if request.method == 'POST':
        openid = request.form.get('openid')
        if openid:
            #request data from provider
            return oid.try_login(openid)
    return render_template('login.html', next = oid.get_next_url(),
            error=oid.get_error())

@oid.after_login
def create_or_login(response):
    """login handler for OpenID, either let them make an account or redirect if they have one"""
    session['openid'] = response.identity_url  #this is the 'key' for a user
    user = None #get this from db
    if user is not None:
        #user already has an acct, let them login
        g.user = user
        return redirect(oid.get_next_url())
    return redirect(url_for('create_account', next = oid.get_next_url())

@app.route('/create/', methods = ['GET', 'POST']):
def create_account():
    """ Prompt the user to make an acct and set feeds if they have not done so yet """
    if g.user is not None or 'openid' not in session:
        return redirect('/')
    if request.method == 'POST':
        #get the feed information that is entered, email, name, etc
        #do validation of required fields
        #create user in DB
        return redirect(oid.get_next_url())
    return render_template('account.html', next = oid.get_next_url())

@app.route('/logout/')
def logout():
    session.pop('openid', None)
    return redirect(oid.get_next_url())


@app.route('/<username>/')
def user_pulse(username):
    context = {
        'username': username,
        'bio': """Edit your bio here, enter some information about you. This is
 customizable and you can add a quote or something here, maybe a link to your
personal site or where you work. It's really up to you!""",

        'pulse_feed': [
            dict(source='github', text='Commited changes to <a>swanson/mongo-overflow</a> repository.'),
            dict(source='hacker-news', text='Posted a comment on <a>Ask HN: What projects are you working on?</a>'),
            dict(source='reddit', text='Posted a comment on <a>Google App Utilities for Python</a>'),
            dict(source='irl', text='Attended <a>2010 SocialDevCamp Chicago Hackathon</a>'),
            ]
        }
    
    return render_template('user_pulse.html', **context)


@app.template_filter()
def timesince(dt, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """
    now = datetime.now()
    diff = now - dt

    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)
    return default


if '__main__' == __name__:
    app.run()
