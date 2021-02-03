<<<<<<< HEAD
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 41,
   "metadata": {},
   "outputs": [],
   "source": [
    "from sqlalchemy import create_engine\n",
    "from sqlalchemy import inspect\n",
    "from sqlalchemy.ext.declarative import declarative_base\n",
    "from sqlalchemy import Column, String, Integer, Date, Float\n",
    "from sqlalchemy.orm import Session\n",
    "from flask import Flask, jsonify, request"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 42,
   "metadata": {},
   "outputs": [],
   "source": [
    "Base = declarative_base()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 43,
   "metadata": {},
   "outputs": [],
   "source": [
    "class Measurement(Base):\n",
    "    __tablename__ = \"measurement\"\n",
    "    \n",
    "    id = Column(Integer, primary_key = True)\n",
    "    station = Column(String)\n",
    "    date = Column(Date)\n",
    "    prcp = Column(Float)\n",
    "    tobs = Column(Float)\n",
    "    \n",
    "class Station(Base):\n",
    "    __tablename__ = \"station\"\n",
    "    \n",
    "    id = Column(Integer, primary_key = True)\n",
    "    station = Column(String)\n",
    "    name = Column(String)\n",
    "    latitude = Column(Float)\n",
    "    longitude = Column(Float)\n",
    "    elevation = Column(Float)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 45,
   "metadata": {},
   "outputs": [
    {
     "ename": "NameError",
     "evalue": "name 'session' is not defined",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mNameError\u001b[0m                                 Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-45-4d60abaf1632>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m      1\u001b[0m \u001b[0mengine\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mcreate_engine\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"sqlite:///Resources/hawaii.sqlite\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      2\u001b[0m \u001b[0mconn\u001b[0m\u001b[0;34m=\u001b[0m \u001b[0mengine\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mconnect\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 3\u001b[0;31m \u001b[0msession\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0msession\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mbind\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mengine\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[0;31mNameError\u001b[0m: name 'session' is not defined"
     ]
    }
   ],
   "source": [
    "engine = create_engine(\"sqlite:///Resources/hawaii.sqlite\")\n",
    "conn= engine.connect()\n",
    "session = session(bind=engine)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [],
   "source": [
    "app = Flask(__name__)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/\")\n",
    "def main():\n",
    "    return(\n",
    "        f\"Welcome to the Climate App Home Page!<br>\"\n",
    "        f\"Available Routes Below:<br>\"\n",
    "        f\"Precipitation measurement over the last 12 months: /api/v1.0/precipitation<br>\"\n",
    "        f\"A list of stations and their respective station numbers: /api/v1.0/stations<br>\"\n",
    "        f\"Temperature observations at the most active station over the previous 12 months: /api/v1.0/tobs<br>\"\n",
    "        f\"Enter a start date (yyyy-mm-dd) to retrieve the minimum, maximum, and average temperatures for all dates after the specified date: /api/v1.0/<start><br>\"\n",
    "        f\"Enter both a start and end date (yyyy-mm-dd) to retrieve the minimum, maximum, and average temperatures for that date range: /api/v1.0/<start><end><br>\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {},
   "outputs": [],
   "source": [
    "# precipation for last 12 months\n",
    "@app.route(\"/api/v1.0/precipation\")\n",
    "def precipitation():\n",
    "    \"\"\"Precipitation from the past 12 months\"\"\"\n",
    "    start_date = max_date - relativedelta(years=1)\n",
    "    end_date = max_date\n",
    "    print(start_date, end_date)\n",
    "    \n",
    "#     date & precip for last year\n",
    "    data = session.query(measurement.date, measurement.rain).filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()\n",
    "    for info in data:\n",
    "        print(info)\n",
    "#     date and prcp as value\n",
    "    rain_df = pd.DataFrame(data, columns =[\"date\", \"rain\"])\n",
    "    rain_df.set_index(\"date\").sort_values\n",
    "    \n",
    "    return jsonify(rain_df)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "metadata": {},
   "outputs": [],
   "source": [
    "# create station route of a list of the stations in the dataset\n",
    "@app.route(\"/api/v1.0/stations\")\n",
    "def stations():\n",
    "    \n",
    "    results = session.query(station.id).all()\n",
    "    \n",
    "    stations = dict(stations)\n",
    "    return jsonify(stations_dict)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "metadata": {},
   "outputs": [],
   "source": [
    "# create tobs route of temp observations for most active stations over last 12 months\n",
    "@app.route(\"/api/v1.0/tobs\")\n",
    "def tobs():\n",
    "    \n",
    "    temp_station = session.query(measurement.date, Measurement.tobs)\\\n",
    "    .filter(Measurement.date > '2016-08-23')\\\n",
    "    .filter(Measurement.date <= '2017-08-23')\\\n",
    "    .filter(Measurement.station == \"USC00519281\")\\\n",
    "    .order_by(Measurement.date).all\n",
    "    \n",
    "    tobs_dict = dict(temp_station)\n",
    "    \n",
    "    return jsonify(tobs_dict)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 38,
   "metadata": {},
   "outputs": [],
   "source": [
    "# create start and end routes\n",
    "# min, avg, max temps for given range\n",
    "@app.route(\"/api/v1.0/<start>\")\n",
    "@app.route(\"/api/v1.0/<start>/<end>\")\n",
    "def start_date(start, end=None):\n",
    "    \n",
    "    q = session.query(str(func.min(Measurement.tobs)), str(func.max(Measurement.tobs)), str(func.round(func.avg(Measurement.tobs))))\n",
    "\n",
    "    if start:\n",
    "        q = q.filter(Measurement.date >= start)\n",
    "\n",
    "    if end:\n",
    "        q = q.filter(Measurement.date <= end)\n",
    "        \n",
    "    results = q.all()[0]\n",
    "\n",
    "    keys = [\"Min Temp\", \"Max Temp\", \"Avg Temp\"]\n",
    "\n",
    "    temp_dict = {keys[i]: results[i] for i in range(len(keys))}\n",
    "\n",
    "    return jsonify(temp_dict)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "metadata": {},
   "outputs": [
    {
     "ename": "SyntaxError",
     "evalue": "invalid syntax (<ipython-input-40-d6fb01e21094>, line 1)",
     "output_type": "error",
     "traceback": [
      "\u001b[0;36m  File \u001b[0;32m\"<ipython-input-40-d6fb01e21094>\"\u001b[0;36m, line \u001b[0;32m1\u001b[0m\n\u001b[0;31m    if__name__ == \"__main__\":\u001b[0m\n\u001b[0m                             ^\u001b[0m\n\u001b[0;31mSyntaxError\u001b[0m\u001b[0;31m:\u001b[0m invalid syntax\n"
     ]
    }
   ],
   "source": [
    "if__name__ == \"__main__\":\n",
    "    app.run(debug=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "environment": {
   "name": "common-cpu.m55",
   "type": "gcloud",
   "uri": "gcr.io/deeplearning-platform-release/base-cpu:m55"
  },
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
=======
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
session = session(bind=engine)

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

if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 6eb567d64e7c91cba767b6ee18ded0fdf69f713c
