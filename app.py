# Import Flask
from flask import Flask, jsonify

import numpy as np
import datetime as dt
from datetime import date, datetime
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect Existing Database Into a New Model
Base = automap_base()
# Reflect the Tables
Base.prepare(engine, reflect=True)

# Save References to Each Table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create Session (Link) From Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Route Setup
@app.route("/")
def main():
    """Lists all available routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

# Create Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
        previous_year = dt.date(2017,8,23) - dt.timedelta(days=365)
        # Design a Query to Retrieve the Last 12 Months of Precipitation Data Selecting Only the `date` and `prcp` Values
        previous_year_prcp = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= previous_year).\
                order_by(Measurement.date).all()
        session.close()
        # Convert  Into a Dictionary
        previous_year_prcp_list = dict(previous_year_prcp)
        return jsonify(previous_year_prcp_list)
        

# Create Station Route
@app.route("/api/v1.0/stations")
def stations():
        # Return JSON List of Stations 
        all_stations = session.query(Station.station, Station.name).all()
        session.close()
        # Convert Into List
        
        station_list=list(np.ravel(all_stations))
        return jsonify(station_list)

# Create TOBs Route
@app.route("/api/v1.0/tobs")
def tobs():
        # Query for the Dates and Temperature Observations from a Year from the Last Data Point
        previous_year = dt.date(2017,8,23) - dt.timedelta(days=365)
        # Design a Query to Retrieve the Last 12 Months of Precipitation Data Selecting Only the `date` and `prcp` Values
        year_tobs = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= previous_year).\
                order_by(Measurement.date).all()
        session.close()
        # Convert Into List
        year_tobs_list = list(np.ravel(year_tobs))
        return jsonify(year_tobs_list)

# Create Start Day Route
@app.route("/api/v1.0/<start>")
def start_day(start):
        start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()
        session.close()
        # Convert Into List
        start_day_list = list(np.ravel(start_day))
        return jsonify(start_day_list)

# Create Start-End Day Route
@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
        start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()
        session.close()
        # Convert Into List
        start_end_day_list = list(np.ravel(start_end_day))
        # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start-End Range
        return jsonify(start_end_day_list)




if __name__ == '__main__':
    app.run(debug=True)


