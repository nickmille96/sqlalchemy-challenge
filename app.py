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



#################################################
# Flask Routes
#################################################
@app.route("/")
def about ():
    routes = /api/v1.0/precipitation

return routes



if __name__ == "__main__":
    app.run(debug=True)
