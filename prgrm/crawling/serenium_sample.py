import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Chrome 웹 브라우저를 실행
with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
    # 암시적 대기
    driver.get("https://indistreet.com/live")
    driver.implicitly_wait(10)

    p = driver.find_element(By.TAG_NAME, 'p').text
    pl = [e.text for e in driver.find_elements(By.TAG_NAME, 'p')]
    print("{}\n{}".format(p, pl))

    # 명시적 대시
    driver.get("https://indistreet.com/live")
    xpath = '//*[@id="__next"]/div/main/div[2]/div/div[4]/div[1]/div[1]/div/a/div[1]/div/span/img'
    first_img = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    print(first_img)

    # 로그인
    driver.get("https://programmers.co.kr/")
    time.sleep(1)

    btn = driver.find_element(By.LINK_TEXT, '로그인')
    ActionChains(driver).click(btn).perform()
    time.sleep(1)

    id_input = driver.find_element(By.CSS_SELECTOR, 'input[type=email]')
    ActionChains(driver).send_keys_to_element(id_input, "your_id").perform()

    pw_input = driver.find_element(By.CSS_SELECTOR, 'input[type=password]')
    ActionChains(driver).send_keys_to_element(pw_input, "your_pw").perform()

    xpath = '//*[@id="main-app-account"]/div/div[2]/div/div[2]/div[1]/div/div[2]/button'
    send_btn = driver.find_element(By.XPATH, xpath)
    ActionChains(driver).click(send_btn).perform()
