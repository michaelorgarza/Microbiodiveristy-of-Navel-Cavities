
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

def SampleNamesCollector():
    sampleNames = []
    for sampleid in session.query(Samples_Metadata.SAMPLEID).all():
        sampleNames.append("BB_"+str(sampleid[0]))
    return jsonify(sampleNames)

####################################

def OTUbySamplesCollector(sample):
    fields = [sample]
    results = session.query(Samples).options(load_only(sample)).order_by(desc(sample))
    
    collector = []
    names = []
    values = []
    
    for result in results[:10]:
        row = result.__dict__    
        names.append(f"Otu - {row['otu_id']}")
        values.append(row[f"{sample}"])
    
    values = [round((x/sum(values))*100,2) for x in values]
        
    return {
        'Name':names,
        'values':values
    }

  



####################################


def SampleMetaDataCollector(sample_id):
    # assign the db's uniform resource identifier to a variable
    db_uri = 'sqlite:///db/belly_button_biodiversity.sqlite'

    #connect to the db using create_engine():
    from sqlalchemy import create_engine
    # returned value engine represents the core interface to the database
    engine = create_engine(db_uri,echo=False)

    # Declare a Base using `automap_base()`
    from sqlalchemy.ext.automap import automap_base
    Base = automap_base()

    # Use the Base class to reflect the database tables
    Base.prepare(engine, reflect=True)

    # mapped classes are now created with names by default
    # matching that of the table name.
    Otu = Base.classes.otu
    Samples = Base.classes.samples
    Samples_Metadata = Base.classes.samples_metadata

    # Create a session
    from sqlalchemy.orm import Session
    session = Session(engine)

    # initialize an empty list to store the sample metadata table
    sampleMetaData = []

    for row in session.query(Samples_Metadata).all():
        sampleMetaData.append(row.__dict__)

    import pandas as pd
    sampleMetaData = pd.DataFrame.from_dict(sampleMetaData, orient='columns', dtype=None)

    sample_id = sampleMetaData

    print(sample_id)
    meta  = sampleMetaData[sampleMetaData['SAMPLEID']==sample_id]
    meta = meta[['AGE','BBTYPE','ETHNICITY','GENDER','LOCATION','SAMPLEID']]

    meta = [{u: str(v)} for (u, v) in meta.iloc[0].iteritems()]
    return meta
    

