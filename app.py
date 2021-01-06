from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Date, Float
from sqlalchemy.orm import Session
from flask import Flask, jsonify, request

Base = declarative_base()

class Measurement(Base):
    __tablename__ = "measurement"
    
    id = Column(Integer, primary_key = True)
    station = Column(String)
    date = Column(Date)
    prcp = Column(Float)
    tobs = Column(Float)
    
class Station(Base):
    __tablename__ = "station"
    
    id = Column(Integer, primary_key = True)
    station = Column(String)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn= engine.connect()
session = session(sessionmake(bind=engine))

app = Flask(__name__)

@app.route("/")
def main():
    return(
        f"Welcome to the Climate App Home Page!<br>"
        f"Available Routes Below:<br>"
        f"Precipitation measurement over the last 12 months: /api/v1.0/precipitation<br>"
        f"A list of stations and their respective station numbers: /api/v1.0/stations<br>"
        f"Temperature observations at the most active station over the previous 12 months: /api/v1.0/tobs<br>"
        f"Enter a start date (yyyy-mm-dd) to retrieve the minimum, maximum, and average temperatures for all dates after the specified date: /api/v1.0/<start><br>"
        f"Enter both a start and end date (yyyy-mm-dd) to retrieve the minimum, maximum, and average temperatures for that date range: /api/v1.0/<start><end><br>")

# precipation for last 12 months
@app.route("/api/v1.0/precipation")
def precipitation():
    """Precipitation from the past 12 months"""
    start_date = max_date - relativedelta(years=1)
    end_date = max_date
    print(start_date, end_date)
    
#     date & precip for last year
    data = session.query(measurement.date, measurement.rain).filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    for info in data:
        print(info)
#     date and prcp as value
    rain_df = pd.DataFrame(data, columns =["date", "rain"])
    rain_df.set_index("date").sort_values
    
    return jsonify(rain_df)

# create station route of a list of the stations in the dataset
@app.route("/api/v1.0/stations")
def stations():
    
    results = session.query(station.id).all()
    
    stations = dict(stations)
    return jsonify(stations_dict)

# create tobs route of temp observations for most active stations over last 12 months
@app.route("/api/v1.0/tobs")
def tobs():
    
    temp_station = session.query(measurement.date, Measurement.tobs)\
    .filter(Measurement.date > '2016-08-23')\
    .filter(Measurement.date <= '2017-08-23')\
    .filter(Measurement.station == "USC00519281")\
    .order_by(Measurement.date).all
    
    tobs_dict = dict(temp_station)
    
    return jsonify(tobs_dict)

# create start and end routes
# min, avg, max temps for given range

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_date(start, end=None):
    
    q = session.query(str(func.min(Measurement.tobs)), str(func.max(Measurement.tobs)), str(func.round(func.avg(Measurement.tobs))))

    if start:
        q = q.filter(Measurement.date >= start)

    if end:
        q = q.filter(Measurement.date <= end)
        
    results = q.all()[0]

    keys = ["Min Temp", "Max Temp", "Avg Temp"]

    temp_dict = {keys[i]: results[i] for i in range(len(keys))}

    return jsonify(temp_dict)
