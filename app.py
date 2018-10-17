import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from flask import Flask, jsonify, render_template, request
import csv


# Create App
app = Flask(__name__)

# Connect to sqlite database
engine = create_engine("sqlite://")
Base = automap_base()
Base.prepare(engine, reflect=True)
session = Session(engine)

# Storing tables
Otu = Base.classes.otu
Samples = Base.classes.samples
Samples_Metadata = Base.classes.samples_metadata