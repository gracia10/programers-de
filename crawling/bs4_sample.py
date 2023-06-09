import requests
from bs4 import BeautifulSoup

url = "https://hashcode.co.kr"
user_agent = {"User-Agent": "*"}
res = requests.get(url, user_agent)

soup = BeautifulSoup(res.text, "html.parser")

r1 = soup.find("li", "question-list-item").find("div", "question").find("div", "top").h4
r2 = soup.select_one("li.question-list-item div.question div.top h4")

soup = BeautifulSoup('<b class="boldest">Extremely bold</b>', 'html.parser')

print(type(soup.b.name))
