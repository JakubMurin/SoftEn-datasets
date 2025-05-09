# Dátum poslednej úpravy sekvenčných diagramov
from utils import *

plt.rc('font', size=12)

fig, axs = plt.subplots(1, 1, figsize=(10, 6))

uc_data = pd.read_csv(UC_CSV_PATH, usecols=["date", "origin"])
seq_data = pd.read_csv(SEQ_CSV_PATH, usecols=["date", "origin"])
data = pd.concat([uc_data, seq_data]).dropna()

data_str = data[data.origin == "github"]["date"].values.astype(str)

date_series = pd.to_datetime(data_str)
date_counts = date_series.to_period('Q').value_counts().sort_index()
print(date_counts.sort_values(ascending=False)[:10])
print(date_series.value_counts().sort_values(ascending=False)[:10])

info = cbook.boxplot_stats(date_counts)
print(f"Median: {date_counts.median()}, Mean: {date_counts.mean()}")
print(f"Q1: {info[0]["q1"]}, Q3: {info[0]["q3"]}")

labels = list(map(lambda x: x.strftime('%F Q%q'), date_counts.index))

axs.bar(labels, date_counts.values)

axs.yaxis.grid(True)
axs.set_ylabel("Počet súborov")

plt.xticks(rotation=80)
plt.tight_layout(pad=1)
plt.savefig(os.path.join(WORKING_DIR, "analysis", "img", "seq_dates.png"), dpi=300)
plt.show()