# Počet alternatívnych scenárov
from utils import *

plt.rc('font', size=15)
fig, axs = plt.subplots()


data = pd.read_csv(UC_CSV_PATH, usecols=["num_of_alt_scenarions"])

graph_values = data["num_of_alt_scenarions"]
info = cbook.boxplot_stats(graph_values)

print(data.value_counts()[:10])
print(f"Median: {data.median()}, Mean: {data.mean()}")
print(f"Q1: {info[0]["q1"]}, Q3: {info[0]["q3"]}")


freq = {}
for i in graph_values:
    freq[i] = freq.get(i, 0) + 1
    
freq = dict(sorted(freq.items()))
plots = axs.bar(freq.keys(), freq.values())

axs.yaxis.grid(True)
axs.set_ylabel("Počet alternatívnych scenárov")
axs.bar_label(plots, fmt='{:,.0f}')

plt.ylim(0, max(freq.values()) * 2.5)
axs.set_yscale('symlog')
plt.tight_layout(pad=1)
plt.savefig(os.path.join(WORKING_DIR, "analysis", "img", "uc_alt_scen.png"), dpi=300)
plt.show()