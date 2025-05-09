# 
import matplotlib.patches as mpatches
from matplotlib.ticker import MaxNLocator
from utils import *

plt.rc('font', size=15)
fig, axs = plt.subplots()

data = pd.read_csv(ALL_CSV_PATH, usecols=["seq_num_of_participats", "uc_actors"])

line = mpatches.Patch(color='C1', label='rovnosť')
plt.legend(handles=[line])

axs.xaxis.set_major_locator(MaxNLocator(integer=True))
axs.yaxis.set_major_locator(MaxNLocator(integer=True))

axs.scatter(x=data["seq_num_of_participats"], y=data["uc_actors"], zorder=5)
axs.plot(range(20), range(20), color="C1", zorder=0)

axs.set_xlabel('Objekty sekvenčného diagramu')
axs.set_ylabel('Aktéri prípadu použitia')

plt.tight_layout(pad=1)
plt.savefig(os.path.join(WORKING_DIR, "analysis", "img", "uc_actors_steps.png"), dpi=300)
plt.show()