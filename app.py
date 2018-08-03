import os

import pandas as pd
import numpy as np
from biofunctions import SampleNamesCollector, OTUbySamplesCollector, SampleMetaDataCollector, idCollectorPC


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import desc
from sqlalchemy.orm import load_only

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

engine = create_engine("sqlite:///db/belly_button_biodiversity.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)


Base.classes.keys()
# ['otu', 'samples', 'samples_metadata']
Samples_Metadata = Base.classes.samples_metadata
Samples = Base.classes.samples
Otu = Base.classes.otu

session = Session(engine)

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/names")
def sampleNames():
    sampleNames = SampleNamesCollector()
    return (sampleNames)

@app.route("/metadata/<sample_id>")
def metaDataSample(sample_id):
    meta = SampleMetaDataCollector(sample_id)
    return jsonify(meta)

@app.route("/otu")
def otu():
    data = idCollectorPC()
    return(data)

@app.route("/samples/<sample>")
def check(sample):
    data = OTUbySamplesCollector(sample)
    return(data)

if __name__ == "__main__":
    app.run(debug=True)

# @app.route("/samples/<sample>")
# def samples(sample):
#     data = biofunctions.PieChart(sample)
#     return(data)

