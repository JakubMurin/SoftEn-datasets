# Rôznorodosť názvov
from utils import *
from wordcloud import WordCloud

uc_data = pd.read_csv(UC_CSV_PATH, usecols=["title"])
seq_data = pd.read_csv(SEQ_CSV_PATH, usecols=["title"])
data = pd.concat([uc_data, seq_data]).dropna()

text = " ".join(title.lower() for title in data["title"].values.astype(str))
freq = {}
for i in text.split():
    freq[i] = freq.get(i, 0) + 1
    
sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
freq = dict(sorted_freq)

wordcloud = WordCloud(background_color="white", width=1600, height=800, stopwords=set(), include_numbers=True).fit_words(freq)
wordcloud.to_file(os.path.join(WORKING_DIR, "analysis", "img", "title_words.png"))

print(sorted_freq[:10])
