#import dependencies
from ML import ML_model,ML_df
classifier = ML_model()
df = ML_df()
import os
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

#from calculator.py
#Define Functions
def calculate(array):
    result = round(100*classifier.predict_proba(array)[0][1],4)
    return result

def change_data(array,index,value):
    temp_arr = array.copy()
    temp_arr[index] = value
    return(temp_arr)

def change_to_YN(value):
    if value == 0:
        return("N")
    if value == 1:
        return("Y")


#Calculate Original %

def origin_prob(customerID):
    output = calculate(df.loc[[customerID]])
    return(output)
    

def compare_scenario(customerID):
    _input = df.loc[[customerID]]
    columns = df.columns
    scenario = {}
    for i in range(23):
        _input = df.loc[[customerID]]
        _input.iloc[:,i] = 1-_input.iloc[:,i]
        scenario[columns[i]+" to "+change_to_YN(_input.iloc[:,i].values[0])] = str(round(origin_prob(customerID) - calculate(_input),4))+"%"
    # print(scenario)
    return scenario

# origin_prob("6713-OKOMC")
# compare_scenario("6713-OKOMC")


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
@app.route('/_get_data/<customerID>')
def get_data_customer(customerID):

   output =  compare_scenario(customerID)
   return jsonify(output)

@app.route('/churn/<customerID>')
def get_churn(customerID):

     churn = origin_prob(customerID)
     return jsonify(churn)

if __name__ == "__main__":
    app.run(debug=True)