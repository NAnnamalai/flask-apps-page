# Using https://api.adviceslip.com/
from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

@app.route("/")
def home():
    url = 'https://api.adviceslip.com/advice'
    response = requests.get(url)
    data = json.loads(response.text)
    return render_template('home.html', advice=data['slip']['advice'])

if __name__ == '__main__':
    app.run(debug=True)