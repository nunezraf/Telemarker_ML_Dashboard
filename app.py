import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from flask import Flask, jsonify, render_template, request
import csv


# Create App
app = Flask(__name__)

# Connect to sqlite database
engine = create_engine("sqlite:///db/telemarker_db.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
session = Session(engine)


# Storing tables# Storing tables
Telemarker_db = Base.classes.telemarker_db

# Returns the dashboard homepage
@app.route("/")
def home():
    return render_template("form.html")


@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        name = request.form["name"]
        

        customerName = Name(name=name)
        db.session.add(name)
        db.session.commit()

        return "Thanks for the form data!"

    return render_template("form.html")

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
    
    # Grab gender column
    results = session.query(Telemarker_db.gender)

    # Loop through query & grab customer gender
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

    # Grab telemarker db table
    customer = session.query(Telemarker_db)

    # Loop through query & grab info
   
    for info in customer:
        if (sample_id == info.SAMPLEID):
            customer_metadata["NAME"] = info.Name
            customer_metadata["CITY"] = info.City
            customer_metadata["ADDRESS"] = info.Address
            customer_metadata["STATE"] = info.State
            customer_metadata["PHONE NUMBER"] = info.Phone
            customer_metadata["GENDER"] = info.GENDER
           

    return jsonify(sample_metadata)

    #Returns a list of phone services
    @app.route("/services/<service>")
    def services(service):

        #create a sample query
        sample_query = "customer." + service

        # create empty dictionary 
        customer_info = {}

        # Grab the info
        results = session.query(customer.cust, sample_query)

        # Loop through & append
        for result in results:
            cust.append(results[0])

        #add to the dictionary
        customer_info = {
            "cust" : cust,
        }

        return jsonify(customer_info)
if __name__ == "__main__":
    app.run(debug=True)