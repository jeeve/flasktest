from flask import Flask, render_template, url_for, request

import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

from .utils import OpenGraphImage

@app.route('/')
@app.route('/index/')
def index():
    page_title = "Le super test flask cool"
    return render_template('index.html', page_title = page_title)

@app.route('/result/')
def result():
    return render_template('result.html')

# @app.route('/contents/<int:content_id>/')
# def content(content_id):
#     return '%s' % content_id

@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
	fig = Figure()
 #   axis = fig.add_subplot(1, 1, 1)
 #   xs = range(100)
 #   ys = [random.randint(1, 50) for x in xs]
 #   axis.plot(xs, ys)
 
	df = pd.read_csv("https://statmeteo.000webhostapp.com/sensations/get-meteo.php")
	df.columns = ['date_heure', 'station', 'vent', 'orientation', 'temperature']
	df["date_heure"] = pd.to_datetime(df["date_heure"], format='%Y-%m-%d %H:%M')
	df[["vent", "orientation", "temperature"]] = df[["vent", "orientation", "temperature"]].apply(pd.to_numeric)
	station = "lusigny-sur-barse" #@param ["louviers", "mantes-la-jolie", "dreux", "montigny-le-bretonneux", "torcy", "montereau-fault-yonne", "lusigny-sur-barse"]

	df_station = df[df['station'] == station]

	is_semaine = df_station['date_heure'] > datetime.now() - timedelta(days=7)
	df_station_semaine = df_station[is_semaine]

	axis = fig.add_subplot(1, 1, 1)
	xs = df_station_semaine['date_heure']
	ys = df_station_semaine['vent']
	axis.scatter(xs, ys)

	return fig