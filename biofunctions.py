
import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import load_only
from sqlalchemy import func, desc

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


####################################

def idCollectorPC():
    all_otus = session.query(Otu).statement
    all_otus_df = pd.read_sql_query(all_otus, session.bind)
    all_otus_df.set_index('otu_id', inplace=True)
    
    return jsonify(list(all_otus_df["lowest_taxonomic_unit_found"]))

# function is functioning

####################################

def subjectCollectorBG(sample_number):
    """returns backgroup info on subjects"""
    sample_id = sample_number[3:]
    results = session.query(Samples_Metadata).filter(Samples_Metadata.SAMPLEID == sample_id).all()
    
    print(results)
    
    return {
        'age':results[3:],
        'gender':results[2:],
        'ethnicity':results[1:],
        'location':results[4:],
        'source':results[5:]
    }
# function is functioning

####################################

def OtuCollectorBC():
    """pulls info for bubble chart"""
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

def idListN():
    columns = Samples.__table__.columns.keys()
    return columns[1:]
# function is functioning

####################################

