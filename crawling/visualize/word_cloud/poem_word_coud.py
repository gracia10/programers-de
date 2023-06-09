import matplotlib.pyplot as plt
from konlpy.tag import Hannanum
from collections import Counter

from matplotlib import font_manager
from wordcloud import WordCloud

with open('poem', 'r') as file:
    poem = file.read()

hnn = Hannanum()
nouns = hnn.nouns(poem)
print(nouns)

counter = Counter(nouns)
print(counter)

# 폰드 가져오기
font_name = "AppleGothic"
font_path = font_manager.FontProperties(fname=font_name + '.ttf').get_file()

# 폰트 사용을 위해 matplotlib 설정
plt.rcParams['font.family'] = font_name

wordcloud = WordCloud(
    font_path=font_path,
    background_color='white'
)
img = wordcloud.generate_from_frequencies(counter)
plt.imshow(img)
plt.show()
