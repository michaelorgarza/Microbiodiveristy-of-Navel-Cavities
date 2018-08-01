
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

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///StarterCode/Belly_Button_Biodiversity/db/belly_button_biodiversity.sqlite"
db = SQLAlchemy(app)
Base = automap_base()
Base.prepare(db.engine, reflect=True)


Base.classes.keys()
# ['otu', 'samples', 'samples_metadata']
Samples_Metadata = Base.classes.samples_metadata
Samples = Base.classes.samples
Otu = Base.classes.otu

session = Session(engine)

####################################

def idCollector (sample_id):
    id = [sample_id]
    results = session.query(Samples).options(load_only(sample_id)).order_by(desc(sample_id))
    
    collector = []
    names = []
    values = []
    
    for result in results[:10]:
        row = result.__dict__    
        names.append(f"Otu - {row['otu_id']}")
        values.append(row[f"{sample_id}"])
    
    values = [round((x/sum(values))*100,2) for x in values]
        
    return {
        'Name':names,
        'values':values
    }
# function is functioning

####################################

def infoCollector(sample_id):
    info_id = sample_id[3:]
    results = session.query(Samples_Metadata).filter(Samples_Metadata.SAMPLEID == info_id).first()
    
    print(results)
    
    return {
        'age':results.AGE,
        'gender':results.GENDER,
        'ethnicity':results.ETHNICITY,
        'location':results.LOCATION,
        'source':results.EVENT
    }
# function is functioning

####################################

def OtuCollector():
    results = session.query(Samples).all()
    x = []
    y = []
    
    for result in results:
        row = result.__dict__
        otu_values = list(row.values())
        x.append(result.otu_id)
        y.append(sum(otu_values[1:]))
        
    return {
        'x':x,
        'y':y
    }
# function is functioning      

####################################

def idList():
    columns = Samples.__table__.columns.keys()
    return columns[1:]
# function is functioning

####################################

