# Korelácia medzi číselnými údajmi
from utils import *
import seaborn

plt.figure(figsize=(9, 7))

data = pd.read_csv(ALL_CSV_PATH, usecols=["uc_temperature", "uc_top_p", "uc_actors", "uc_num_of_steps", "uc_num_of_alt_scenarions",
                                          "uc_num_of_err_scenarions", "seq_temperature", "seq_top_p", "seq_actors",
                                          "seq_num_of_participats", "seq_num_of_alt", "seq_num_of_opt", "seq_num_of_loop", "uc_origin", "seq_origin"])


data["uc_temperature"] = data["uc_temperature"].replace(0, np.nan)
data["uc_top_p"] = data["uc_top_p"].replace(0, np.nan)
data["seq_temperature"] = data["seq_temperature"].replace(0, np.nan)
data["seq_top_p"] = data["seq_top_p"].replace(0, np.nan)

corr = data.corr(numeric_only=True)
print(corr)

axs = seaborn.heatmap(corr, center=0, cmap='RdBu_r', annot=False)
axs.xaxis.tick_top()
axs.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)

plt.xticks(fontsize=15, rotation=45, ha="left")
plt.yticks(fontsize=15)

plt.tight_layout(pad=1)
plt.savefig(os.path.join(WORKING_DIR, "analysis", "img", "correl.png"), dpi=300)
plt.show()