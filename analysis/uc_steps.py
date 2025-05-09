# Počet krokov prípadu použitia
from utils import *

plt.rc('font', size=15)
fig, axs = plt.subplots()


data = pd.read_csv(UC_CSV_PATH, usecols=["num_of_steps"])

info = cbook.boxplot_stats(data)
graph_values = data[data.num_of_steps < 100]["num_of_steps"]

h, x = np.histogram(graph_values, bins=30)
print(*h, sep="\t")
print(*np.round(x), sep="\t")
print(data.value_counts()[:10])
print(f"Median: {data.median()}, Mean: {data.mean()}")
print(f"Q1: {info[0]["q1"]}, Q3: {info[0]["q3"]}")

plots = axs.hist(graph_values, bins=30)

axs.yaxis.grid(True)
axs.set_xlabel("Počet krokov")
axs.set_ylabel("Počet výskytov")

plt.tight_layout(pad=1)
plt.savefig(os.path.join(WORKING_DIR, "analysis", "img", "uc_steps.png"), dpi=300)
plt.show()