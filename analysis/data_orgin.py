# Pôvod záznamov

from utils import *

plt.rc('font', size=15)

fig, axs = plt.subplots()

labels = ["Sekvenčný\ndiagram", "Prípad\npoužitia"]
uc_data = pd.read_csv(UC_CSV_PATH, usecols=["origin"])
seq_data = pd.read_csv(SEQ_CSV_PATH, usecols=["origin"])

uc_gpt, uc_github = uc_data.value_counts("origin")
seq_github, seq_gpt = seq_data.value_counts("origin")

axs.bar(labels, [seq_github, seq_gpt])
axs.bar(labels, [seq_github, seq_gpt], bottom=[seq_github, seq_gpt])

axs.yaxis.grid(True)
axs.set_ylabel('Počet súborov')
axs.set_yscale('symlog')

plt.legend(["GitHub", "ChatGPT"])
plt.tight_layout(pad=1)
plt.savefig(os.path.join(WORKING_DIR, "analysis", "img", "data_origin.png"), dpi=300)
plt.show()