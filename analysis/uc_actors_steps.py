# Závislosť objektov sekvenčného diagramu a aktérov prípadu použitia
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import MaxNLocator
from utils import *

plt.rc('font', size=17)
fig, axs = plt.subplots()

data = pd.read_csv(ALL_CSV_PATH, usecols=["seq_num_of_participats", "uc_actors"])

axs.xaxis.set_major_locator(MaxNLocator(integer=True))
axs.yaxis.set_major_locator(MaxNLocator(integer=True))

count_data = data.value_counts().reset_index(name='frequency')

custom_cmap = LinearSegmentedColormap.from_list('custom', ['black', "red", 'orange'])
scatter = axs.scatter(count_data["seq_num_of_participats"], count_data["uc_actors"], c=count_data["frequency"],
            s=count_data["frequency"], cmap=custom_cmap, alpha=0.8)

cbar = plt.colorbar(scatter)

axs.set_xlabel('Počet objektov sekvenčného diagramu')
axs.set_ylabel('Počet aktérov prípadu použitia')
axs.set_xticks(range(0, 19, 3), range(0, 19, 3))
axs.set_yticks(range(0, 19, 3), range(0, 19, 3))

plt.tight_layout(pad=1)
plt.savefig(os.path.join(WORKING_DIR, "analysis", "img", "uc_actors_steps.png"), dpi=300)
plt.show()