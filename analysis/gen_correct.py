# Korektnosť generovaných dát
import matplotlib.patches as mpatches
from matplotlib.ticker import MaxNLocator
from utils import *

plt.rc('font', size=11)
fig, axs = plt.subplots()

uc_data = pd.read_csv(UC_CSV_PATH, usecols=["temperature", "top_p", "origin"])
seq_data = pd.read_csv(SEQ_CSV_PATH, usecols=["temperature", "top_p", "origin"])
data = pd.concat([uc_data, seq_data])

deta = data[data.origin == "chatgpt"]

temp_data = data[(data.temperature != 1) & (data.top_p == 1)]
top_data = data[(data.temperature == 1) & (data.top_p != 1)]
def_data = data[(data.temperature == 1) & (data.top_p == 1)]

te_06 = len(temp_data[temp_data.temperature == 0.6].values)
te_08 = len(temp_data[temp_data.temperature == 0.8].values)
te_12 = len(temp_data[temp_data.temperature == 1.2].values)
te_14 = len(temp_data[temp_data.temperature == 1.4].values)
to_02 = len(top_data[top_data.top_p == 0.2].values)
to_04 = len(top_data[top_data.top_p == 0.4].values)
to_06 = len(top_data[top_data.top_p == 0.6].values)
to_08 = len(top_data[top_data.top_p == 0.8].values)
defau = len(def_data.values)

graph_data = np.array([te_06, te_08, te_12, te_14, to_02, to_04, to_06, to_08]) / 948 * 100
graph_data = np.append(graph_data, [100 * defau / (2 * 948)])
print(graph_data)

colors = ["C0", "C0", "C0", "C0", "C1", "C1", "C1", "C1", "C2"]
names = ["0.6", "0.8", "1.2", "1.4", "0.2", "0.4", "0.6 ", "0.8 ", "1"]
temp = mpatches.Patch(color='C0', label='temperature')
top = mpatches.Patch(color='C1', label='top_p')
default = mpatches.Patch(color='C2', label='základná')
legend = plt.legend(handles=[temp, top, default], loc="lower left")
legend.get_frame().set_alpha(None)

# int y values
axs.yaxis.set_major_locator(MaxNLocator(integer=True))

plots = axs.bar(names, graph_data, color=colors)

axs.bar_label(plots, fmt='{:,.0f}%')
axs.set_xticks(range(9), names)
axs.yaxis.grid(True)
axs.set_xlabel("Hodnota parametra")
axs.set_ylabel('Úspešnosť')

plt.ylim(top=100)
plt.savefig(os.path.join(WORKING_DIR, "analysis", "img", "gen_correct.png"), dpi=300)
plt.show()