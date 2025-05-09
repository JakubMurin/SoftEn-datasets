# Počet výnimkových scenárov
from utils import *

plt.rc('font', size=15)
fig, axs = plt.subplots()


data = pd.read_csv(UC_CSV_PATH, usecols=["num_of_err_scenarions"])

graph_values = data["num_of_err_scenarions"]
info = cbook.boxplot_stats(graph_values)

print(data.value_counts()[:10])
print(f"Median: {data.median()}, Mean: {data.mean()}")
print(f"Q1: {info[0]["q1"]}, Q3: {info[0]["q3"]}")


freq = {}
for i in graph_values:
    freq[i] = freq.get(i, 0) + 1
    
freq = dict(sorted(freq.items()))
plots = axs.bar(freq.keys(), freq.values(), color="C1")

axs.yaxis.grid(True)
axs.set_xlabel("Počet výnimkových scenárov")
axs.set_ylabel("Počet výskytov")
axs.bar_label(plots, fmt='{:,.0f}')

plt.ylim(0, max(freq.values()) * 2.5)
axs.set_yscale('symlog')
plt.tight_layout(pad=1)
plt.savefig(os.path.join(WORKING_DIR, "analysis", "img", "uc_err_scen.png"), dpi=300)
plt.show()