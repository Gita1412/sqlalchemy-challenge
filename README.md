# sqlalchemy-challenge
Steps : 
1. Download the Module 10 Challenge files
2. There are 2 parts:
   - Part 1 : Analyze and Explore the Climate Data
   - Part 2 : Design Climate App
  
Part 1 : Analyze and Explore the Climate Data
Steps :
1. In this section, the analyst will use SQLAlchemy ORM queries, Pandas, Matplotlib.
2. Basic analysis :
   - Use the SQLAlchemy create_engine() function to connect to SQLite database.
   - Use the SQLAlchemy automap_base() function to reflect tables into classes, and then save references to the classes named station and measurement.
   - Link Python to the database by creating a SQLAlchemy session.
3. Precipitation Analysis
   - Find the most recent date in the dataset.
   - Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.
   - Select only the "date" and "prcp" values.
   - Load the query results into a Pandas DataFrame. Explicitly set the column names.
   - Sort the DataFrame values by "date".
   - Plot the results by using the DataFrame plot method.
   - Use Pandas to print the summary statistics for the precipitation data.
4. Station Analysis
   - Design a query to calculate the total number of stations in the dataset.
   - Design a query to find the most-active stations (that is, the stations that have the most rows).
   - Design a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.
   - Design a query to get the previous 12 months of temperature observation (TOBS) data.


Part 2 : Design Climate App
Steps : 
1. In this section, the analyst will design a Flask API based on the query that has been developed.
2. (/)
   - Start at the homepage.
   - List all the available routes.
3. (/api/v1.0/precipitation)
   - Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
   - Return the JSON representation of your dictionary.
4. (/api/v1.0/stations)
   - Return a JSON list of stations from the dataset.
5. (/api/v1.0/tobs)
   - Query the dates and temperature observations of the most-active station for the previous year of data.
   - Return a JSON list of temperature observations for the previous year.
6. (/api/v1.0/<start> and /api/v1.0/<start>/<end>)
   - Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
   - For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
   - For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
















