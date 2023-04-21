# 기상청 데이터 크롤링
import seaborn as sns
from matplotlib import pyplot as plt

from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

url = "https://www.weather.go.kr/w/index.do"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)
driver.implicitly_wait(1)

temps = driver.find_element(By.ID, "my-tchart").text
temps = [int(n) for n in temps.replace('℃', '').split('\n')]
print(temps)

plt.title("Expected Temperature from now on")
plt.ylim(min(temps) - 5, max(temps) + 5)
sns.lineplot(x=range(len(temps)), y=temps)
plt.show()
