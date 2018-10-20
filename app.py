import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from flask import Flask, jsonify, render_template, request
import csv


# Create App
app = Flask(__name__)

# Connect to sqlite database
engine = create_engine("sqlite:///dataset/telemarker_db.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
session = Session(engine)


# Storing tables# Storing tables
Telemarker_db = Base.classes.telemarker_db
# Samples = Base.classes.samples
# Samples_Metadata = Base.classes.samples_metadata

# Returns the dashboard homepage
@app.route("/")
def home():
    return render_template("index.html")

# Returns a list of customer_ids in list format
@app.route("/customer_ids")
def customer_ids():

    # Empty list for sample ids
    customer_ids = []
    
    # Grab metadata table
    results = session.query(Telemarker_db.customerID)

    # Loop through query & grab ids
    for result in results:
        customer_ids.append(str(result[0]))

    return jsonify(customer_ids)


# Returns a list of customer gender
@app.route("/gender")
def gender():

    # Empty list for descriptions
    customer_gender = []
    
    # Grab otu table
    results = session.query(Telemarker_db.gender)

    # Loop through query & grab descriptions
    for result in results:
        customer_gender.append(str(result[0]))

    return jsonify(customer_gender)

# Returns a json dictionary of sample metadata
@app.route("/metadata/<customer>")
def metadata(customerINFO):
    
    # Grab input
    customer_info = int(customerINFO.split("_")[1])

    # Empty dictionary for data
    customer_metadata = {}

    # Grab metadata table
    customer = session.query(Telemarker_db)

    # Loop through query & grab info
    # this is where ryou need to change
    for info in customer:
        if (sample_id == info.SAMPLEID):
            sample_metadata["AGE"] = info.AGE
            sample_metadata["BBTYPE"] = info.BBTYPE
            sample_metadata["ETHNICITY"] = info.ETHNICITY
            sample_metadata["GENDER"] = info.GENDER
            sample_metadata["LOCATION"] = info.LOCATION
            sample_metadata["SAMPLEID"] = info.SAMPLEID

    return jsonify(sample_metadata)