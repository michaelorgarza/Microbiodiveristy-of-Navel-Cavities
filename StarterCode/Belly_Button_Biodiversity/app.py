import os

import pandas as pd
import numpy as np
from StarterCode.Belly_Button_Biodiversity import biofunctions


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/names")
def names():
    data = biofunctions.idList()
    return jsonify(data)

@app.route("/samples/<sample>")
def sample(sample_id):
    info = biofunctions.infoCollector(sample_id)
    otu_coll = biofunctions.OtuCollector(sample_id)
    otu_id = biofunctions.idCollector(sample_id)
    data = {
        'info': info,
        'otu_descr': otu_coll,
        'otu_value': otu_id
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)

# @app.route("/metadata/<sample>")
# def sample_metadata(sample):
#     """Return the MetaData for a given sample."""
#     sel = [
#         Samples_Metadata.sample,
#         Samples_Metadata.ETHNICITY,
#         Samples_Metadata.GENDER,
#         Samples_Metadata.AGE,
#         Samples_Metadata.LOCATION,
#         Samples_Metadata.BBTYPE,
       
#     ]

#     results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

#     # Create a dictionary entry for each row of metadata information
#     sample_metadata = {}
#     for result in results:
#         sample_metadata["sample"] = result[0]
#         sample_metadata["ETHNICITY"] = result[1]
#         sample_metadata["GENDER"] = result[2]
#         sample_metadata["AGE"] = result[3]
#         sample_metadata["LOCATION"] = result[4]
#         sample_metadata["BBTYPE"] = result[5]
        

#     print(sample_metadata)
#     return jsonify(sample_metadata)
