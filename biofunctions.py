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

# create instance of Flask app
app = Flask(__name__)

# setup database
engine = create_engine("sqlite:///db/belly_button_biodiversity.sqlite", echo=False)

Base = automap_base()
Base.prepare(engine, reflect=True)
Sample = Base.classes.samples
OTU = Base.classes.otu
Metadata = Base.classes.samples_metadata


session = Session(engine)


def nameCollector():
    """ returns sample ID's and sets as index"""
    samples = session.query(Sample).statement
    samples_df = pd.read_sql_query(samples, session.bind)
    samples_df.set_index('otu_id', inplace=True)
    return jsonify(list(samples_df.columns))

def otuCollector():
    """ returns Otu (bacteria taxonomy)info"""
    otus = session.query(OTU).statement
    otus_df = pd.read_sql_query(otus, session.bind)
    otus_df.set_index('otu_id', inplace=True)
    return jsonify(list(otus_df["lowest_taxonomic_unit_found"]))

def metaCollector(sample):
    """returns metadata info (e.g., descriptive stats) on BB samples"""
    samples_meta = session.query(Metadata).statement
    samples_meta_df = pd.read_sql_query(samples_meta, session.bind)
    sample_name = int(sample.split("_")[1])
    selected_sample = samples_meta_df.loc[samples_meta_df["SAMPLEID"] == sample_name, :]
    json_selected_sample = selected_sample.to_json(orient='records')
    return json_selected_sample

def washingCollector(sample):
    """ returns washing frequency info from samples"""
    samples_meta = session.query(Metadata).statement
    samples_meta_df = pd.read_sql_query(samples_meta, session.bind)
    sample_name = int(sample.split("_")[1])
    selected_sample = samples_meta_df.loc[samples_meta_df["SAMPLEID"] == sample_name, :]
    wfreq = selected_sample["WFREQ"].values[0]
    return wfreq

def sampleCollector(sample):
    """ returns sample info """
    otus = session.query(OTU).statement
    otus_df = pd.read_sql_query(otus, session.bind)
    otus_df.set_index('otu_id', inplace=True)

    samples = session.query(Sample).statement
    samples_df = pd.read_sql_query(samples, session.bind)
    selected_sample = samples_df[sample]
    otu_ids = samples_df['otu_id']
    selection_df = pd.DataFrame({
        "otu_ids":otu_ids,
        "samples":selected_sample
    })
    sorted_df = selection_df.sort_values(by=['samples'], ascending=False)
    sorted_otus = {"otu_ids": list(sorted_df['otu_ids'].values)}
    sorted_samples = {"sample_values": list(sorted_df['samples'].values)}
    for i in range(len(sorted_otus["otu_ids"])):
        sorted_otus["otu_ids"][i] = int(sorted_otus["otu_ids"][i])
    for i in range(len(sorted_samples["sample_values"])):
        sorted_samples["sample_values"][i] = int(sorted_samples["sample_values"][i])
    results = [sorted_otus, sorted_samples, list(otus_df["lowest_taxonomic_unit_found"])]
    return jsonify(results)




