# Import the dependencies.
import matplotlib
from matplotlib import style
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
M = Base.classes.measurement
S = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return(
        f"Welcome!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prcp_data = (
        session.query(M.date, M.prcp)
        .filter(M.date > "2017-08-23")
        .order_by(M.date)
        .all()
    )
    session.close()
    prcp_results = []
    for data in prcp_data:
        prcp_results.append(data)
    prcp = dict(prcp_results)
    return jsonify(prcp)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    sel = [S.station,S.name,S.latitude,S.longitude,S.elevation]
    queryresult = session.query(*sel).all()
    session.close()

    stations = []
    for station,name,lat,lon,el in queryresult:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Lat"] = lat
        station_dict["Lon"] = lon
        station_dict["Elevation"] = el
        stations.append(station_dict)

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    tobs_data = (
        session.query(M.date, M.tobs)
        .filter(M.station == "USC00519281")
        .filter(M.date > "2017-08-23")
    )
    tobs_results = []
    for tob in tobs_data:
        tobs_results.append(tob)
    session.close()
    temperature_data = dict(tobs_results)
    return jsonify(temperature_data)

@app.route("/api/v1.0/<start>")
def get_t_start(start):
    session = Session(engine)
    queryresult = session.query(func.min(M.tobs), func.avg(M.tobs), func.max(M.tobs)).\
        filter(M.date >= start).all()
    session.close()

    tobsall = []
    for min,avg,max in queryresult:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobsall.append(tobs_dict)

    return jsonify(tobsall)

@app.route("/api/v1.0/<start>/<end>")
def get_t_start_stop(start,stop):
    session = Session(engine)
    queryresult = session.query(func.min(M.tobs), func.avg(M.tobs), func.max(M.tobs)).\
        filter(M.date >= start).filter(M.date <= stop).all()
    session.close()

    tobsall = []
    for min,avg,max in queryresult:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobsall.append(tobs_dict)

    return jsonify(tobsall)


if __name__ == "__main__":
    app.run(debug=True)