# Dátum poslednej úpravy sekvenčných diagramov
from utils import *

plt.rc('font', size=12)

fig, axs = plt.subplots(1, 1, figsize=(10, 6))

data = pd.read_csv(SEQ_CSV_PATH, usecols=["date"])

data_str = data["date"].values.astype(str)

date_series = pd.to_datetime(data_str)
date_counts = date_series.to_period('Q').value_counts().sort_index()
print(date_series.value_counts().sort_values())

labels = list(map(lambda x: x.strftime('%F Q%q'), date_counts.index))

axs.bar(labels, date_counts.values)

axs.yaxis.grid(True)
axs.set_ylabel("Počet súborov")

plt.xticks(rotation=80)
plt.tight_layout(pad=1)
plt.savefig(os.path.join(WORKING_DIR, "analysis", "img", "seq_dates.png"), dpi=300)
plt.show()