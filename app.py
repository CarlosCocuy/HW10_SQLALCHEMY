from flask import Flask, jsonify
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

#Flask set up
app = Flask(__name__)


#flask pages
#Home
@app.route("/")
def Home():
    return (
        f"List of routes<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/(start)             put a value in for start in YYYY-MM-DD no()<br/>"
        f"/api/v1.0/(start)/(end)       put a value in for start and end in YYYY-MM-DD no()"
   )

@app.route("/api/v1.0/precipitation")
def precipitation():

    #Convert the query results to a Dictionary using date as the key and prcp as the value.
    #Return the JSON representation of your dictionary.

    past_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Perform a query to retrieve the date and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= past_date).all()
    prec=list(np.ravel(results))

    return jsonify(prec)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    #Return a JSON list of stations from the dataset.
    results = session.query(Station.station,Station.name).all()
    sta = list(np.ravel(results))

    return jsonify(sta)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    #query for the dates and temperature observations from a year from the last data point.
    #Return a JSON list of Temperature Observations (tobs) for the previous year.
    past_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Perform a query to retrieve the date and precipitation scores
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= past_date).all()
    temp=list(np.ravel(results))

    return jsonify(temp)

@app.route("/api/v1.0/<start>")
def temperature_start(start):
    session = Session(engine)
    result= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
    .filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).all()
    temperature_stats= list(np.ravel(result))
    return jsonify(temperature_stats)


@app.route("/api/v1.0/<start>/<end>")
def temperature_stat_end(start,end):
    session = Session(engine)
    result= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
    .filter(func.strftime("%Y-%m-%d", Measurement.date) >= start).filter(func.strftime("%Y-%m-%d", Measurement.date) <= end).all()
    temperature_stats= list(np.ravel(result))
    return jsonify(temperature_stats)
if __name__ == "__main__":
    app.run(debug=True)
