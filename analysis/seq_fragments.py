# Fragmenty sekvenčného diagramu

import matplotlib.patches as mpatches
from utils import *

def freq(graph_values):
    freq = {}
    for i in graph_values:
        freq[i] = freq.get(i, 0) + 1
        
    return dict(sorted(freq.items()))

plt.rc('font', size=15)
fig, axs = plt.subplots()

data = pd.read_csv(SEQ_CSV_PATH, usecols=["num_of_alt", "num_of_opt", "num_of_loop"])


colors = ["C0", "C1", "C2"]
names = ["alt", "opt", "loop"]
alt = mpatches.Patch(color='C0', label='alternatíva')
opt = mpatches.Patch(color='C1', label='podmienka')
loop = mpatches.Patch(color='C2', label='cyklus')
plt.legend(handles=[alt, opt, loop])

alt_data = freq(data["num_of_alt"])
opt_data = freq(data["num_of_opt"])
loop_data = freq(data["num_of_loop"])

print(f"alt: {alt_data} = {sum(alt_data.values()) - alt_data[0]}", 
      f"opt: {opt_data} = {sum(opt_data.values()) - opt_data[0]}", 
      f"loop {loop_data} = {sum(loop_data.values()) - loop_data[0]}", sep="\n")

alt_data.pop(0)
opt_data.pop(0)
loop_data.pop(0)


axs.bar(np.array(list(alt_data.keys()))-0.2, alt_data.values(), width=0.2, align='center')
axs.bar(opt_data.keys(), opt_data.values(), width=0.2, align='center')
axs.bar(np.array(list(loop_data.keys()))+0.2, loop_data.values(), width=0.2, align='center')

plt.xticks(range(1, 13))

axs.yaxis.grid(True)
axs.set_ylabel('Počet výskytov')
axs.set_yscale('log')

plt.tight_layout(pad=1)
plt.savefig(os.path.join(WORKING_DIR, "analysis", "img", "seq_fragments.png"), dpi=300)
plt.show()