import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

WORKING_DIR = os.getcwd()
ALL_CSV_PATH = os.path.join(WORKING_DIR, "all.csv")

df = pd.read_csv(ALL_CSV_PATH)

# Inicializácia štýlu pre seaborn
sns.set_theme(style="whitegrid")

# Vytvorenie troch grafov: boxplot a dva violin ploty
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 2. Violin plot: seq_temperature podľa seq_ai_model
a = sns.violinplot(ax=axes[0], data=df, x='seq_temperature', y='seq_actors')
a.set(yscale="log")
axes[0].set_title("Teplota generovania podľa AI modelu (SEQ)")

# 3. Violin plot: seq_num_of_participats podľa seq_ai_model
sns.violinplot(ax=axes[1], data=df, x='uc_temperature', y='uc_actors')
axes[1].set_title("Počet účastníkov v sekvencii podľa AI modelu")

# 1. Boxplot: uc_num_of_steps podľa origin
sns.boxplot(ax=axes[2], data=df, x='origin', y='uc_num_of_steps')
axes[2].set_title("Počet krokov v UC podľa pôvodu")

# Zobrazenie grafov
# sns.set_style(None)
# plt.tight_layout()
plt.show()