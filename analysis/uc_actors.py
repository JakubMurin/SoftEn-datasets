# Počet aktérov prípadu použitia
from utils import *

plt.rc('font', size=15)
fig, axs = plt.subplots()


data = pd.read_csv(UC_CSV_PATH, usecols=["actors"])

graph_values = data["actors"]
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
axs.set_xlabel("Počet aktérov")
axs.set_ylabel("Počet výskytov")


plt.tight_layout(pad=1)
plt.savefig(os.path.join(WORKING_DIR, "analysis", "img", "uc_actors.png"), dpi=300)
plt.show()