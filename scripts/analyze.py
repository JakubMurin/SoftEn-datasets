import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ydata_profiling as pp

from utils import jsonl_to_csv

WORKING_DIR = os.getcwd()
ALL_FLAT_JSON_PATH = os.path.join(WORKING_DIR, "test", "flat_all.jsonl")
ALL_CSV_PATH = os.path.join(WORKING_DIR, "test", "all.csv")

# jsonl_to_csv(ALL_FLAT_JSON_PATH, ALL_CSV_PATH)

data =pd.read_csv(ALL_CSV_PATH)

data.info()

pp.ProfileReport(data, title="test", ).to_file("report.html")