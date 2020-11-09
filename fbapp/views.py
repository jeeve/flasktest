from flask import Flask, render_template, url_for, request

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

from .utils import OpenGraphImage

@app.route('/')
@app.route('/index/')
def index():
    page_title = "Le test ultime"
    return render_template('index.html')

@app.route('/result/')
def result():
    return render_template('result.html')

# @app.route('/contents/<int:content_id>/')
# def content(content_id):
#     return '%s' % content_id
