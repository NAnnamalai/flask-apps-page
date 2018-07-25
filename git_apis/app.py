import requests
import requests_cache
from flask import Flask, render_template, request, redirect, url_for
import logging

app = Flask(__name__)

requests_cache.install_cache('github_cache', backend='sqlite', expire_after=1800)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html')

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/home', methods=['GET', 'POST'])
def home():
    github_uname = request.form.get("github_uname")
    if github_uname:

        # get all the public repos of a user
        repo_url = 'https://api.github.com/users/' + github_uname + '/repos'

        # make a api request, also cache it to ensure the same username is served from cache
        # https://realpython.com/caching-external-api-requests/
        repo_response = requests.get(repo_url)

        following_url = 'https://api.github.com/users/' + github_uname + '/following'
        following_response = requests.get(following_url)

        followers_url = 'https://api.github.com/users/' + github_uname + '/followers'
        followers_response = requests.get(followers_url)

        info_flag = True
    else:
        info_flag = False
        repo_response = {}
        following_response = {}
        followers_response = {}
    return render_template('home.html', repo_info=repo_response, 
                                        following_info=following_response,
                                        followers_info=followers_response,
                                        info_flag=info_flag)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


if __name__ == "__main__":
    # app.debug = True
    logging.basicConfig(filename='error.log',level=logging.DEBUG)
    app.run(host='0.0.0.0', port=5000)