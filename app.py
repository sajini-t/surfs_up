# Added Dependencies
#-------------------
import datetime as dt
import numpy as np
import pandas as pd

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# import dependencies for flask
from flask import Flask, jsonify



# Set up our database engine for the Flask application
#-----------------------------------------------------
# Code to access SQLite Database
# create_engine() function allows us to access and query our SQLite database file
engine = create_engine("sqlite:///hawaii.sqlite")

# transfer the contents of the database into a different structure of data
Base = automap_base()

# reflect the tables with prepare() function
Base.prepare(engine, reflect=True)

# save references to eacg table with a variable
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database
session = Session(engine)

# Define app for Flask application
#---------------------------------
# __name__ variable in this code. This is a special type of variable in Python.
# Its value depends on where and how the code is run. When we run python app.py, 
# the __name__ variable will be set to __main__

# All of your routes should go after the app = Flask(__name__) line of code
app = Flask(__name__)

# naming convention for routes /api/v1.0/ followed by the name of the route
# This convention signifies that this is version 1 of our application

@app.route("/")
def welcome():
    return('''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    # we'll create a dictionary with the date as the key and the precipitation as the value.
    # To do this, we will use Jsonify() function that converts the dictionary to a JSON file
    precip = {date: prcp for date, prcp in precipitation}   
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    # unraveling our results query into a one-dimensional array using np.ravel() function
    # Convert that array into a list using list() function
    stations = list(np.ravel(results))
    return jsonify(stations=stations)


@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)










