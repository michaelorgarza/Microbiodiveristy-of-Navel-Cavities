#################################################
# Import Dependencies
#################################################
import numpy as np
import pandas as pd

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

##################################################
# flask setup
##################################################
app = Flask(__name__)

##################################################
# database setup
##################################################
engine = create_engine("sqlite:///db/belly_button_biodiversity.sqlite", echo=False)

# reflect an existing database into a new model
# save references to each table
Base = automap_base()
Base.prepare(engine, reflect=True)
Sample = Base.classes.samples
OTU = Base.classes.otu
Metadata = Base.classes.samples_metadata

session = Session(engine)


#################################################
# route setup
##################################################
import biofunctions

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/names')
def names():
    names = biofunctions.nameCollector()
    return(names)

@app.route('/otu')
def otu():
    otu = biofunctions.otuCollector()
    return(otu)

@app.route('/metadata/<sample>')
def metadata(sample):
    metadata = biofunctions.metaCollector(sample)
    return(metadata)

@app.route('/wfreq/<sample>')
def wfreq(sample):
    wfreq = biofunctions.washingCollector(sample)
    return(wfreq)

@app.route('/samples/<sample>')
def samples(sample):
    samples = biofunctions.sampleCollector(sample)
    return(samples)

if __name__ == "__main__":
    app.run(debug=True)
