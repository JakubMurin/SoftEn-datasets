# Počet krokov prípadu použitia
import matplotlib.patches as mpatches
from matplotlib.ticker import MaxNLocator
from utils import *

plt.rc('font', size=12)

fig, axs = plt.subplots()

data = pd.read_csv(UC_CSV_PATH, usecols=["temperature", "top_p", "num_of_steps", "origin"])
deta = data[data.origin == "chatgpt"]
temp_data = data[(data.temperature != 1) & (data.top_p == 1)]
top_data = data[(data.temperature == 1) & (data.top_p != 1)]
def_data = data[(data.temperature == 1) & (data.top_p == 1)]

colors = ["C0", "C0", "C0", "C0", "C1", "C1", "C1", "C1", "C2"]
names = ["0.6", "0.8", "1.2", "1.4", "0.2", "0.4", "0.6", "0.8", "1"]
temp = mpatches.Patch(color='C0', label='temperature')
top = mpatches.Patch(color='C1', label='top_p')
default = mpatches.Patch(color='C2', label='základná')
legend = plt.legend(handles=[temp, top, default], loc="upper center")
legend.get_frame().set_alpha(None)

# int y values
axs.yaxis.set_major_locator(MaxNLocator(integer=True))

plots = axs.violinplot(dataset=[
    temp_data[temp_data.temperature == 0.6]["num_of_steps"].values,
    temp_data[temp_data.temperature == 0.8]["num_of_steps"].values,
    temp_data[temp_data.temperature == 1.2]["num_of_steps"].values,
    temp_data[temp_data.temperature == 1.4]["num_of_steps"].values,
    top_data[top_data.top_p == 0.2]["num_of_steps"].values,
    top_data[top_data.top_p == 0.4]["num_of_steps"].values,
    top_data[top_data.top_p == 0.6]["num_of_steps"].values,
    top_data[top_data.top_p == 0.8]["num_of_steps"].values,
    def_data["num_of_steps"].values
], showmeans=False, showmedians=True)

plots['cmedians'].set_color('black')
plots['cmedians'].set_linestyle(':')
for pc, color in zip(plots['bodies'], colors):
    pc.set_facecolor(color)

axs.set_xticks(range(1, 10), names)

axs.yaxis.grid(True)
axs.set_ylabel('Počet krokov')
axs.set_ylim(top=25)
axs.set_ybound(0)
# axs.set_yscale('log')

# plt.gca().yaxis.set_major_locator(LogLocator(base=2, subs='auto', numticks=100))
plt.savefig(os.path.join(WORKING_DIR, "analysis", "img", "uc_steps_gen.png"), dpi=300)
plt.show()