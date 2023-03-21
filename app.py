# import dependants
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

# flask setup
app = Flask(__name__)

# homepage route
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-8-23<br/>"
        f"/api/v1.0/2016-8-23/2017-8-23"
    )

query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# precipitation route
@app.route("/api/v1.0/precipitation")
def prcp():
    # query to get data and precipitation values from Measurement table
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= query_date)

    # Create a dictionary from the data
    precipitation = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # query to get list of stations from Station table
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()

    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    active_station = 'USC00519281'
    session = Session(engine)
    results = session.query(Measurement.tobs).\
            filter(Measurement.date >= query_date).\
            filter_by(station = active_station).all()
    session.close()

    tobs = list(np.ravel(results))

    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def start_range(start):
    start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()

    if start_date > dt.date(2017, 8, 23):
        return jsonify({"error": f"{start} exceeds the maximum date in the dataset."}), 404

    session = Session(engine)
    lowest = session.query(func.min(Measurement.tobs)).\
            filter(Measurement.date >= start_date).first()
    highest = session.query(func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).first()
    average = session.query(func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start_date).first()
    session.close()

    list=[]
    list.append(lowest[0])
    list.append(average[0])
    list.append(highest[0])

    return jsonify(list)

@app.route("/api/v1.0/<start>/<end>")
def date_range(start, end):
    start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()
    end_date = dt.datetime.strptime(end, "%Y-%m-%d").date()

    if start_date > dt.date(2017, 8, 23):
        return jsonify({"error": f"{start} exceeds the maximum date in the dataset."}), 404

    session = Session(engine)
    lowest = session.query(func.min(Measurement.tobs)).\
            filter(Measurement.date >= start_date).\
            filter(Measurement.date <= end_date).first()
    highest = session.query(func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).\
            filter(Measurement.date <= end_date).first()
    average = session.query(func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start_date).\
            filter(Measurement.date <= end_date).first()
    session.close()

    list=[]
    list.append(lowest[0])
    list.append(average[0])
    list.append(highest[0])

    return jsonify(list)

if __name__ == '__main__':
    app.run(debug=True)