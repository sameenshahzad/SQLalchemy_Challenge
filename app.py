#import the dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/><br/>Precipitation Analysis for the last 12 months in Hawaii<br/>"
        f"/api/v1.0/precipitation<br/><br/>List of all stations<br/>"
        f"/api/v1.0/stations<br/><br/>Dates and temperature observations of the most-active station for the previous year<br/>"
        f"/api/v1.0/tobs<br/><br/>Minimum temperature, the average temperature, and the maximum temperature<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation and date for the last 12 months"""
    # Query only the last 12 months of data (precipitation and date)
    # Calculate the date one year from the last date in data set.
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date = dt.datetime.strptime(most_recent_date, "%Y-%m-%d")
    one_year_ago = most_recent_date - dt.timedelta(days=365)
    one_year_ago

    results = session.query(Measurement.date,func.avg(Measurement.prcp)).filter(Measurement.date >= one_year_ago).group_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into dictionary
    precipitation_last_12=[]
    for date,prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        precipitation_last_12.append(precipitation_dict)

    return jsonify(precipitation_last_12)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.id,Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).all()
    session.close()
    all_station=[]
    for id,station,name,latitude,longitude,elevation in results:
        station_dict={}
        station_dict['Id']=id
        station_dict['station']=station
        station_dict['name']=name
        station_dict['latitude']=latitude
        station_dict['longitude']=longitude
        station_dict['elevation']=elevation
        all_station.append(station_dict)
    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def temp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the dates and temperature observations of the most-active station for the previous year of data.
    results= session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    session.close()

    temperature=[]
    for tobs,date in results:
        tobs_dict={}
        tobs_dict['date']=date
        tobs_dict['tobs']=tobs
        temperature.append(tobs_dict)
    return jsonify(temperature)


 # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
 # This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
 # and return the minimum, average, and maximum temperatures for that range of dates  

@app.route("/api/v1.0/<start>")
def calc_temps_sd(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date == start).all()

    session.close()

    temp_observe={}
    temp_observe["Min_Temp"]=results[0][0]
    temp_observe["avg_Temp"]=results[0][1]
    temp_observe["max_Temp"]=results[0][2]
    return jsonify(temp_observe)


@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date == start).filter(Measurement.date <= end).all()

    session.close()

    temp_ob={}
    temp_ob["Min_Temp"]=results[0][0]
    temp_ob["avg_Temp"]=results[0][1]
    temp_ob["max_Temp"]=results[0][2]
    return jsonify(temp_ob)

if __name__ == '__main__':
    app.run(debug=True)