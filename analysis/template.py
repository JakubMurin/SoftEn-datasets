from utils import *

fig, axs = plt.subplots()

data = pd.read_csv(UC_CSV_PATH, usecols=["temperature", "top_p", "actors"])
# temp_data = data[(data.temperature != 1) & (data.top_p == 1)]


plots = axs.bar()

axs.yaxis.grid(True)
axs.set_ylabel('')

plt.legend(["", ""])
plt.tight_layout(pad=1)
plt.savefig(os.path.join(WORKING_DIR, "analysis", "img", "tmp.png"), dpi=300)
plt.show()