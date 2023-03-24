# SQLalchemy_Challenge

## Part 1 : Analyze and Explore the Climate Data

Use Python and SQLAlchemy to do a basic climate analysis and data exploration of the climate database. 

### Precipitation Analysis

- Find the most recent date in the dataset.
- Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.
- Select only the "date" and "prcp" values.
- Load the query results into a Pandas DataFrame, and set the index to the "date" column.
- Sort the DataFrame values by "date".
- Plot the results by using the DataFrame plot method
- Use Pandas to print the summary statistics for the precipitation data.




### Station Analysis

- Design a query to calculate the total number of stations in the dataset.
- Design a query to find the most-active stations (that is, the stations that have the most rows). List the stations and observation counts in descending order.
- Design a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.
- Design a query to get the previous 12 months of temperature observation (TOBS) data. To do so, complete the following steps:
  - Filter by the station that has the greatest number of observations.
  - Query the previous 12 months of TOBS data for that station.
  - Plot the results as a histogram with bins=12


## Part 2: Design A Climate App
