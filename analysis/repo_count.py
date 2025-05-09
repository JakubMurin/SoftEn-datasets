# Početnosť podľa repozitára
from utils import *

uc_data = pd.read_csv(UC_CSV_PATH, usecols=["repo"])
seq_data = pd.read_csv(SEQ_CSV_PATH, usecols=["repo"])

merge = pd.concat([uc_data, seq_data])

print(merge.value_counts("repo")[:20])