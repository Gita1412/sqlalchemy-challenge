# Import the dependencies
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import scoped_session, sessionmaker
import datetime as dt



#################################################
# Database Setup
#################################################

# Create an engine to the SQLite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={"check_same_thread": False})

# Reflect the database into a new model
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a scoped session to ensure thread safety
Session = scoped_session(sessionmaker(bind=engine))

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Home Route
@app.route('/')
def home():
    return jsonify({
        "Available Routes": [
            "/api/v1.0/precipitation",
            "/api/v1.0/stations",
            "/api/v1.0/tobs",
            "/api/v1.0/2016-08-24", #start date
            "/api/v1.0/2016-08-24/2017-08-23" #start date / end date
        ]
    })

# Precipitation Route
@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session()
    try:
        # Get the last date and calculate one year before
        last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
        one_year_ago = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=365)

        # Query for the last year's precipitation data
        results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()

        # Format data as dictionary
        precipitation_data = {date: prcp for date, prcp in results}
        return jsonify(precipitation_data)
    finally:
        session.close()

# Stations Route
@app.route('/api/v1.0/stations')
def stations():
    session = Session()
    try:
        # Query all stations
        results = session.query(Station.station).all()
        # Convert results to a list
        stations_list = [station[0] for station in results]
        return jsonify(stations_list)
    finally:
        session.close()

# Temperature Observations Route
@app.route('/api/v1.0/tobs')
def tobs():
    session = Session()
    try:
        # Define the most active station
        most_active_station = 'USC00519281'

        # Get the last date and calculate one year before
        last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
        one_year_ago = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=365)

        # Query temperature observations for the most active station
        results = session.query(Measurement.tobs).filter(Measurement.station == most_active_station).filter(Measurement.date >= one_year_ago).all()
        # Convert results to a list
        tobs_list = [temp[0] for temp in results]
        return jsonify(tobs_list)
    finally:
        session.close()
        
        
# Dynamic Start Date Route
@app.route('/api/v1.0/<start>')
def start_date(start):
    session = Session()
    try:
        # Validate the start date
        try:
            start_date = dt.datetime.strptime(start.strip(), "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

        # Query for min, avg, and max temperatures from the start date onward
        results = session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        ).filter(Measurement.date >= start_date).all()

        # Check if results exist
        if not results or results[0][0] is None:
            return jsonify({"error": "No data found for the given start date"}), 404

        # Return results as JSON
        return jsonify({
            "start_date": start,
            "TMIN": results[0][0],
            "TAVG": results[0][1],
            "TMAX": results[0][2]
        })
    finally:
        session.close()

# Dynamic Start and End Date Route
@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start, end):
    session = Session()
    try:
        # Validate the start and end dates
        try:
            start_date = dt.datetime.strptime(start.strip(), "%Y-%m-%d")
            end_date = dt.datetime.strptime(end.strip(), "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

        # Ensure the start date is not after the end date
        if start_date > end_date:
            return jsonify({"error": "Start date cannot be after end date"}), 400

        # Query for min, avg, and max temperatures within the date range
        results = session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        ).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

        # Check if results exist
        if not results or results[0][0] is None:
            return jsonify({"error": "No data found for the given date range"}), 404

        # Return results as JSON
        return jsonify({
            "start_date": start,
            "end_date": end,
            "TMIN": results[0][0],
            "TAVG": results[0][1],
            "TMAX": results[0][2]
        })
    finally:
        session.close()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
