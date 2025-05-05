import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ydata_profiling as pp

from utils import jsonl_to_csv

WORKING_DIR = os.getcwd()
ALL_FLAT_JSON_PATH = os.path.join(WORKING_DIR, "data", "results", "all.jsonl")
ALL_CSV_PATH = os.path.join(WORKING_DIR, "all.csv")

columns = [
    # "id",   #
    # "name",   #
    # "origin", #
    # "uc_id",  #
    "uc_file",    #
    "uc_date",
    "uc_origin",
    "uc_source_url",  #
    "uc_repo",
    # "uc_ai_model",    #
    "uc_temperature",
    "uc_top_p",
    # "uc_title",   #
    "uc_actors",
    "uc_num_of_steps",
    "uc_num_of_alt_scenarions",
    "uc_num_of_err_scenarions",
    # "seq_id", #
    "seq_file",   #
    "seq_date",
    "seq_origin",
    # "seq_source_url", #
    "seq_repo",
    # "seq_ai_model",   #
    "seq_temperature",
    "seq_top_p",
    "seq_actors",
    "seq_num_of_participats",
    # "seq_title",  #
    "seq_num_of_alt",
    "seq_num_of_opt",
    "seq_num_of_loop"
]
# jsonl_to_csv(ALL_FLAT_JSON_PATH, ALL_CSV_PATH)

data =pd.read_csv(ALL_CSV_PATH, usecols=columns)

data.info()

pp.ProfileReport(data, title="Dataset analysis", ).to_file("dupp_report.html")