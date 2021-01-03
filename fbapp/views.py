from flask import Flask, render_template, url_for, request

import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import numpy as np
from windrose import WindroseAxes

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

stations = [{'name':'louviers'}, {'name':'mantes-la-jolie'}, {'name':'dreux'}, {'name':'torcy'}, {'name':'montereau-fault-yonne'}, {'name':'lusigny-sur-barse'}]
variables = [{'name':'temperature'}, {'name':'vent'}, {'name':'orientation'}]

station = stations[1]
variable = variables[0]

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html', station=station, variable=variable, stations=stations, variables=variables)
    
@app.route('/result/', methods=['GET', 'POST'])
def result():
    s = request.form.get('station_select')
    v = request.form.get('variable_select')
    global station
    global variable
    station = s
    variable = v
    return render_template('result.html', station=s, variable=v, stations=stations, variables=variables)   

@app.route('/plot/<station>/<variable>/<date>/')
def plot_png_date(station, variable, date):
    fig = create_plot_date(station, variable, date)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/plot/<station>/<variable>/')
def plot_png(station, variable):
    fig = create_plot_date(station, variable, "")
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/rose/<station>/<date>/')
def rose_png_date(station, date):
    fig = create_rose_date(station, date)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/rose/<station>/')
def rose_png(station):
    fig = create_rose_date(station, "")
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/niveau/')
def niveau_png():
    fig = create_niveau()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_niveau():
    df = pd.read_csv("https://statmeteo.000webhostapp.com/sensations/get-niveau.php")    
    df.columns = ['date_heure', 'station', 'hauteur']
    df["date_heure"] = pd.to_datetime(df["date_heure"], format='%Y-%m-%d %H:%M')
    df[["hauteur"]] = df[["vent", "orientation", "temperature"]].apply(pd.to_numeric)
      
    fig = Figure()
    fig.set_size_inches(10, 7, forward=True)
    fig.suptitle(station)

    axis = fig.add_subplot(1, 1, 1)
    xs = df_station['date_heure']
    ys = df_station['hauteur']
    
    axis.set_xlabel('date')
    axis.set_ylabel('hauteur')

    axis.grid()
"""    
    if len(date) == 8:
        axis.set_xlabel(date[6:8] + '/' + date[4:6] + '/' + date[0:4])
        xfmt = mdates.DateFormatter("%H:%M")
        axis.xaxis.set_major_formatter(xfmt)
"""    
    axis.plot(xs, ys)

    return fig 

def create_plot_date(station, variable, date):
    if date == "":
        df = pd.read_csv("https://statmeteo.000webhostapp.com/sensations/get-meteo.php")    
    else:                         
        df = pd.read_csv("https://statmeteo.000webhostapp.com/sensations/get-meteo.php?date=" + date)
    df.columns = ['date_heure', 'station', 'vent', 'orientation', 'temperature']
    df["date_heure"] = pd.to_datetime(df["date_heure"], format='%Y-%m-%d %H:%M')
    df[["vent", "orientation", "temperature"]] = df[["vent", "orientation", "temperature"]].apply(pd.to_numeric)
    
    df_station = df[df['station'] == station]
    
    fig = Figure()
    fig.set_size_inches(10, 7, forward=True)
    fig.suptitle(station)

    axis = fig.add_subplot(1, 1, 1)
    xs = df_station['date_heure']
    ys = df_station[variable]
    
    axis.set_xlabel('date')
    axis.set_ylabel(variable)

    axis.grid()
    
    if len(date) == 8:
        axis.set_xlabel(date[6:8] + '/' + date[4:6] + '/' + date[0:4])
        xfmt = mdates.DateFormatter("%H:%M")
        axis.xaxis.set_major_formatter(xfmt)
    
    axis.plot(xs, ys)

    return fig 

def create_rose_date(station, date):
    if date == "":
        df = pd.read_csv("https://statmeteo.000webhostapp.com/sensations/get-meteo.php")    
    else:                         
        df = pd.read_csv("https://statmeteo.000webhostapp.com/sensations/get-meteo.php?date=" + date)
    df.columns = ['date_heure', 'station', 'vent', 'orientation', 'temperature']
    df["date_heure"] = pd.to_datetime(df["date_heure"], format='%Y-%m-%d %H:%M')
    df[["vent", "orientation", "temperature"]] = df[["vent", "orientation", "temperature"]].apply(pd.to_numeric)
    
    df_station = df[df['station'] == station]
    
    fig = Figure()
    fig.set_size_inches(7, 7, forward=True)
    fig.suptitle(station)


    ax = fig.add_subplot(1, 1, 1, projection="windrose")    
    wd = df_station['orientation']
    ws = df_station['vent']
    ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
    ax.set_legend()
    
    return fig