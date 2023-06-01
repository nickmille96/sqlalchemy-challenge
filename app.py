# Import the dependencies.
import sqlalchemy
from flask import Flask, jsonify
import datetime as dt
import numpy as np
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func 


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
autobase= automap_base()
# reflect an existing database into a new model
autobase.prepare(engine, reflect=True)
# reflect the tables

measurement=autobase.classes.measurement
station=autobase.classes.station



# Create our session (link) from Python to the DB
session= Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
    )
#Temp Route
@app.route("/api/v1.0/precipitation")
def precipation():
  
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    pre_year= dt.date(2017,8,23)- dt.timedelta(days=365)
    results =session.query(measurement.date, measurement.prcp).filter(measurement.date >= pre_year).all()

    session.close()

    # Convert list of tuples into normal list
    precipation = list(np.ravel(results))

    return jsonify(precipation)
#Stations Route.
@app.route("/api/v1.0/stations")
def Station ():
  
    # Create our session (link) from Python to the DB
    session = Session(engine)

    statations =session.query(measurement.station, func.count(measurement.station)).group_by(
    measurement.station).order_by(func.count(measurement.station).desc()).all()

    session.close()

    # Convert list of tuples into normal list
    Station= list(np.ravel(statations))

    return jsonify(Station)

#Query the dates and temperature observations of the most-active station for the previous year of data.
@app.route("/api/v1.0/tobs")
def tobs ():
  
    # Create our session (link) from Python to the DB
    session = Session(engine)
    pre_year= dt.date(2017,8,23)- dt.timedelta(days=365)
    lastyear_temp= session.query(measurement.station, measurement.tobs).\
    filter(measurement.date >= '2016-08-23')\
    .filter(measurement.station == 'USC00519281')\
    .all()

    session.close()

    # Convert list of tuples into normal list
    tobs= list(np.ravel(lastyear_temp))

    return jsonify(tobs)

# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
@app.route("/api/v1.0/<start>", defaults = {"end" : None})
@app.route("/api/v1.0/<start>/<end>")

def tempreturn ():

    session = Session(engine)

    tempr= [func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]

#With Start and end date 
    if end !=None:
       statusr= session.query(*tempr).filter(measurement.date >=start).\
        filter(measurement.date <= end).all()
       temp= list(np.ravel(statusr))
    
    else:
        statusr= session.query(*tempr).filter(measurement.date >=start).\
        filter(measurement.date <= end).all()

    session.close()

# Convert into list

Tlist= []
tdata= False
for TMIN, TAVG, TMAX in tdata:
    if TMIN == None or TAVG == None or TMAX ==None:
        tdata= True
    Tlist.append(TMIN)
    Tlist.append(TAVG)
    Tlist.append(TMAX)




if __name__ == "__main__":
    app.run(debug=True)
