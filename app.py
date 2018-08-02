import os

import pandas as pd
import numpy as np
import biofunctions


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
def names():
    data = biofunctions.idListN()
    return jsonify(data)

@app.route("/metadata/<sample_number>")
def metadata(sample_number):
    data = biofunctions.subjectCollectorBG(sample_number)
    return jsonify(data)

@app.route("/otu")
def otu():
    data = biofunctions.idCollectorPC()
    return(data)

@app.route("/samples")
def samples():
   data = biofunctions.OtuCollectorBC()
   return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)

