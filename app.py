import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/telemarker_db.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Telemarkers = Base.classes.telemarker_db
# field1s = Base.classes.field1s

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/names")
def names():
    """Return a list of field1 names."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(Telemarkers).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (field1 names)
    return jsonify(list(df["customerID"]))

@app.route("/metadata/<field1>")
def telemarker_db(field1):
    """Return the MetaData for a given field1."""
    sel = [
        Telemarkers.customerID,	
        Telemarkers.gender,
        Telemarkers.fName,
        Telemarkers.fAddress,
        Telemarkers.fCity,
        Telemarkers.fState,
        Telemarkers.fPhone,                                               
        Telemarkers.SeniorCitizen,
        Telemarkers.Partner,
        Telemarkers.Dependents,
        Telemarkers.tenure,
        Telemarkers.PhoneService,
        Telemarkers.MultipleLines,        
        Telemarkers.InternetService,
        Telemarkers.OnlineSecurity,
        Telemarkers.OnlineBackup,
        Telemarkers.DeviceProtection,
        Telemarkers.TechSupport,
        Telemarkers.StreamingTV,
        Telemarkers.StreamingMovies,                                                
        Telemarkers.Contract,
        Telemarkers.PaperlessBilling,
        Telemarkers.PaymentMethod,
        Telemarkers.MonthlyCharges,
        Telemarkers.TotalCharges,
        Telemarkers.Churn

    ]

    results = db.session.query(*sel).filter(Telemarkers.field1 == field1).all()

    # Create a dictionary entry for each row of metadata information
    telemarker_db = {}
    for result in results:
        telemarker_db["customerID"] = result[0]
        telemarker_db["gender"] = result[1]
        telemarker_db["fName"] = result[2]
        telemarker_db["fAddress"] = result[3]
        telemarker_db["fCity"] = result[4]
        telemarker_db["fState"] = result[5]
        telemarker_db["fPhone"] = result[7]
        telemarker_db["SeniorCitizen"] = result[8]
        telemarker_db["Partner"] = result[9]
        telemarker_db["Dependents"] = result[10]
        telemarker_db["tenure"] = result[11]
        telemarker_db["PhoneService"] = result[12]
        telemarker_db["MultipleLines"] = result[13]
        telemarker_db["InternetService"] = result[14]                        
        telemarker_db["OnlineSecurity"] = result[15]        
        telemarker_db["OnlineBackup"] = result[16]        
        telemarker_db["DeviceProtection"] = result[17]        
        telemarker_db["TechSupport"] = result[18]        
        telemarker_db["StreamingTV"] = result[19]        
        telemarker_db["StreamingMovies"] = result[20]        
        telemarker_db["Contract"] = result[21]        
        telemarker_db["PaperlessBilling"] = result[22]        
        telemarker_db["PaymentMethod"] = result[23]        
        telemarker_db["MonthlyCharges"] = result[24]        
        telemarker_db["TotalCharges"] = result[25]        
        telemarker_db["Churn"] = result[26]        

    print(telemarker_db)
    return jsonify(telemarker_db)


# @app.route("/field1s/<field1>")
# def field1s(field1):
#     """Return `otu_ids`, `otu_labels`,and `field1_values`."""
#     stmt = db.session.query(field1s).statement
#     df = pd.read_sql_query(stmt, db.session.bind)

#     # Filter the data based on the field1 number and
#     # only keep rows with values above 1
#     field1_data = df.loc[df[field1] > 1, ["otu_id", "otu_label", field1]]
#     # Format the data to send as json
#     data = {
#         "otu_ids": field1_data.otu_id.values.tolist(),
#         "field1_values": field1_data[field1].values.tolist(),
#         "otu_labels": field1_data.otu_label.tolist(),
#     }
#     return jsonify(data)


if __name__ == "__main__":
    app.run()