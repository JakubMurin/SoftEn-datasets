import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cbook

WORKING_DIR = os.getcwd()
ALL_CSV_PATH = os.path.join(WORKING_DIR, "analysis", "all.csv")
UC_CSV_PATH = os.path.join(WORKING_DIR, "analysis", "uc.csv")
SEQ_CSV_PATH = os.path.join(WORKING_DIR, "analysis", "seq.csv")