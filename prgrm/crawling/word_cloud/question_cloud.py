import time
from collections import Counter

from bs4 import BeautifulSoup
import requests
from konlpy.tag import Hannanum
from matplotlib import pyplot as plt, font_manager
from wordcloud import WordCloud


def extract() -> list:
    """
    질문 페이지를 순회해 질문 제목를 수집한다
    :return: 질문 제목 list
    """
    questions = []

    for i in range(1, 6):
        res = requests.get("https://hashcode.co.kr?page={}".format(i))
        soup = BeautifulSoup(res.text, "html.parser")

        parsed_datas = soup.find_all("li", "question-list-item")

        for data in parsed_datas:
            questions.append(data.h4.text.strip())
        time.sleep(0.5)

    return questions


def transfer(questions: list):
    hannanum = Hannanum()
    words = []

    for question in questions:
        nouns = hannanum.nouns(question)
        words += nouns

    counter = Counter(words)
    return counter


def visualize(counter: Counter):
    font_name = "AppleGothic"
    font_path = font_manager.FontProperties(fname=font_name + '.ttf').get_file()
    plt.rcParams['font.family'] = font_name

    wordcloud = WordCloud(
        font_path=font_path,
        background_color='white',
    )

    img = wordcloud.generate_from_frequencies(counter)
    plt.imshow(img)
    plt.show()


datas = extract()
word_counter = transfer(datas)
visualize(word_counter)
