# Počet objektov v sekvenčnom diagrame
from utils import *

plt.rc('font', size=15)
fig, axs = plt.subplots()


data = pd.read_csv(SEQ_CSV_PATH, usecols=["num_of_participats"])

graph_values = data["num_of_participats"]
info = cbook.boxplot_stats(graph_values)

print(data.value_counts())
print(f"Median: {data.median()}, Mean: {data.mean()}")
print(f"Q1: {info[0]["q1"]}, Q3: {info[0]["q3"]}")


freq = {}
for i in graph_values:
    freq[i] = freq.get(i, 0) + 1
    
freq = dict(sorted(freq.items()))
plots = axs.bar(freq.keys(), freq.values())

axs.yaxis.grid(True)
axs.set_ylabel("Počet objektov")

plt.tight_layout(pad=1)
plt.savefig(os.path.join(WORKING_DIR, "analysis", "img", "seq_objects.png"), dpi=300)
plt.show()