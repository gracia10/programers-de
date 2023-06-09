# webhook.site 으로 실습 진행
import requests

url = "https://www.google.com"  # 프로토콜을 빼면 requests.exceptions.MissingSchema 에러 발생
res = requests.get(url)
print(res)

url = "https://webhook.site/8512616d-1e46-4924-a6ce-1f5dcbf50973"
payload = {"name": "Nine", "number": "9"}
res = requests.post(url, payload)
print(res.status_code)
