import os
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

#################################################
# Flask Setup
#################################################

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
# cust_ids = Base.classes.cust_ids

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/id")
def id():
    """Return a list of customer id."""

    # Use Pandas to perform the sql query
    stmt = db.session.query(Telemarkers).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (customer id)
    return jsonify(list(df["customerID"]))

@app.route("/metadata/<customerID>")
def telemarker_db(customerID):
    """Return the MetaData for a given customerID."""
    sel = [
        Telemarkers.customerID, 
        Telemarkers.gender,
        Telemarkers.Name,
        Telemarkers.Address,
        Telemarkers.City,
        Telemarkers.State,
        Telemarkers.Phone,
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

    ]

    results = db.session.query(*sel).filter(Telemarkers.customerID == customerID).all()

    # Create a dictionary entry for each row of metadata information
    telemarker_db = {}
    for result in results:
        telemarker_db["customerID"] = result[0]
        telemarker_db["gender"] = result[1]
        telemarker_db["Name"] = result[2]
        telemarker_db["Address"] = result[3]
        telemarker_db["City"] = result[4]
        telemarker_db["State"] = result[5]
        telemarker_db["Phone"] = result[6]
        telemarker_db["Senior Citizen"] = result[7]
        telemarker_db["Partner"] = result[8]
        telemarker_db["Dependents"] = result[9]
        telemarker_db["tenure"] = result[10]
        telemarker_db["Phone Service"] = result[11]
        telemarker_db["Multiple Lines"] = result[12]
        telemarker_db["Online Security"] = result[14]
        telemarker_db["Online Backup"] = result[15] 
        telemarker_db["Device Protection"] = result[16] 
        telemarker_db["Tech Support"] = result[17]
        telemarker_db["Streaming TV"] = result[18] 
        telemarker_db["Streaming Movies"] = result[19] 
        telemarker_db["Contract"] = result[20]
        telemarker_db["PaperlessBilling"] = result[21]
        telemarker_db["PaymentMethod"] = result[22]      

    print(telemarker_db)


    return jsonify(telemarker_db)

@app.route("/samples/<customerID>")
def samples(customerID):
    """Return `otu_ids`, `otu_labels`,and `sample_values`."""
    stmt = db.session.query(Telemarkers).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Filter the data based on the customerID number and
    # only keep rows with values above 1
    sample_data = df.loc[df[customerID] > 1, [customerID]]
    # Format the data to send as json
    data = {
        # "otu_ids": sample_data.otu_id.values.tolist(),
        "sample_values": sample_data[customerID].values.tolist(),
        # "otu_labels": sample_data.otu_label.tolist(),
    }
    return jsonify(data)

 

if __name__ == "__main__":
    app.run()