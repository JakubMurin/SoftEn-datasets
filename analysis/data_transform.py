import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import ydata_profiling as pp

WORKING_DIR = os.getcwd()
ALL_FLAT_JSON_PATH = os.path.join(WORKING_DIR, "data", "results", "all.jsonl")
ALL_CSV_PATH = os.path.join(WORKING_DIR, "all.csv")
ALL_CSV_PATH = os.path.join(WORKING_DIR, "uc.csv")

fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))

data = pd.read_csv(ALL_CSV_PATH)
# data.info()
# pp.ProfileReport(data, title="Dataset analysis", ).to_file("dupp_report.html")


# generate some random test data
all_data = [np.random.normal(0, std, 100) for std in range(6, 10)]

# plot violin plot
axs[0].violinplot(all_data,
                  showmeans=False,
                  showmedians=True)
axs[0].set_title('Violin plot')

# plot box plot
axs[1].boxplot(all_data)
axs[1].set_title('Box plot')

# adding horizontal grid lines
for ax in axs:
    ax.yaxis.grid(True)
    ax.set_xticks([y + 1 for y in range(len(all_data))],
                  labels=['x1', 'x2', 'x3', 'x4'])
    ax.set_xlabel('Four separate samples')
    ax.set_ylabel('Observed values')

plt.show()