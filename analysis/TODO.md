- zvlast topp, temperature, default a dokopy pre jednotlive pocty (kroky, aktery, objekty, ...)
- zvlast uc a seq pre generovane

- z pohladu top_p a temperature jednotlivo hodnoty

- pre jednotlive hodnoty top_p a temperature, koľko bolo vadlidných odpovedí


Boxplot: uc_num_of_steps podľa uc_origin
→ porovnanie počtu krokov v scenári medzi rôznymi typmi pôvodu dát.

Violin plot: seq_temperature podľa seq_ai_model
→ ako sa teploty generovania líšia medzi modelmi.

Boxplot: uc_num_of_alt_scenarions podľa uc_ai_model (alebo jeho absencie)
→ rozdiely v komplexnosti generovaných prípadov.

Distribučné grafy (box / violin / histogramy)
Violin plot: uc_temperature podľa uc_origin
→ Ako sa líšia teploty generovania pre rôzne zdroje use-caseov (napr. github vs chatgpt).

Boxplot: seq_num_of_loop podľa seq_ai_model
→ Porovnanie zložitosti (cyklickosť) sekvencií v závislosti od použitého modelu.

Histogram: uc_num_of_steps
→ Rozloženie počtu krokov v scenároch – pomôže identifikovať typický rozsah.

Boxplot: seq_num_of_participats podľa uc_actors
→ Ako počet účastníkov v sekvencii súvisí s počtom aktérov v scenári.