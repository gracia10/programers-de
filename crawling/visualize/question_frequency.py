import time
from collections import Counter

import seaborn as sns
from bs4 import BeautifulSoup
import requests
from matplotlib import pyplot as plt


def scrape() -> dict:
    """
    질문 페이지를 순회해 태깅된 태그를 수집한다
    :return: 태그 dict
    """
    frequency = {}

    for i in range(1, 11):
        res = requests.get("https://hashcode.co.kr?page={}".format(i))
        soup = BeautifulSoup(res.text, "html.parser")

        ul_tags = soup.find_all("ul", "question-tags")
        for ul in ul_tags:
            li_tags = ul.find_all("li")
            for li in li_tags:
                lang = li.text.strip()
                if lang not in frequency:
                    frequency[lang] = 1
                else:
                    frequency[lang] += 1

        time.sleep(0.5)

    return frequency


def visualize(top10: list):
    x = [e[0] for e in top10]
    y = [e[1] for e in top10]

    plt.figure(figsize=(20, 10))
    plt.title("Frequency of qustion in hashcode")
    plt.xlabel("Tag")
    plt.ylabel("Frequency")

    sns.barplot(x=x, y=y)

    plt.show()


frequency = scrape()
counter = Counter(frequency)
top10 = counter.most_common(10)
visualize(top10)
