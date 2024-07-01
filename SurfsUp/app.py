# Import the dependencies.
import numpy as np
import sqlalchemy
from flask import Flask, jsonify
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
    # Find the most recent date in the data set.
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # convert to datetime
    recent_date_value = dt.date(2017, 8, 23)

    prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= previous_year).order_by(Measurement.date).all()


    # Convert data into a dictionary
    prcp_dict = {date: prcp for date, prcp in prcp_data}

    session.close()

    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():

    results = session.query(Station.station).all()


    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    session.close()

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query the dates and temperature observations of the most-active station for the previous year of data.
    most_active_station = session.query(Measurement.station, func.count(Measurement.station)).\
                    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()[0]
    
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    tobs_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= previous_year).order_by(Measurement.date).all()

    tobs_list = [{"date": date, "tobs": tobs} for date, tobs in tobs_data]

    session.close()

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start):
    # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    
    temp_data = session.query(func.min(Measurement.tobs),
                     func.max(Measurement.tobs),
                     func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    
    temps = {
        "TMIN": temp_data[0][0],
        "TMAX": temp_data[0][1],
        "TAVG": temp_data[0][2]
    }
    
    session.close()
    
    return jsonify(temps)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    
    temp_data = session.query(func.min(Measurement.tobs),
                     func.max(Measurement.tobs),
                     func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    temps = {
        "TMIN": temp_data[0][0],
        "TMAX": temp_data[0][1],
        "TAVG": temp_data[0][2]
    }

    session.close()
    
    return jsonify(temps)



if __name__ == '__main__':
    app.run(debug=True)
