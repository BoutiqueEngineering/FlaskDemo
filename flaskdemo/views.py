
from flask import Flask, flash, redirect, render_template, \
     request, session, url_for

from flaskdemo import app
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def baf_render_template(template, **kwargs):
    if 'username' in session:
      kwargs['username'] = session['username']
    return render_template(template, **kwargs)

@app.route('/')
def index():
    return baf_render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                request.form['password'] != 'secret':
            error = 'Invalid credentials'
        else:
            flash('You were successfully logged in')
            return redirect(url_for('index'))
    return baf_render_template('login.html', error=error)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

if __name__ == "__main__":
    app.run()
