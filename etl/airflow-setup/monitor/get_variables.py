import logging

import requests
from requests import HTTPError, JSONDecodeError
from requests.auth import HTTPBasicAuth

url = "http://localhost:8080/api/v1/variables"


def get_variables():
    """
        Airflow Config 조회하는 함수
        - (사전 작업) config API 접근 허용 -> webserver 의 expose_config, True
    """
    res = requests.get(url, auth=HTTPBasicAuth("airflow", "airflow"))

    # http 통신 응답값 검증
    try:
        res.raise_for_status()
        variables = res.json()
        if variables.get('variables') is None:
            raise KeyError(variables)
    except (HTTPError, JSONDecodeError) as e:
        logging.warning(f'오류가 발생했습니다. 상태 코드: {e.response.status_code}')
        raise
    except KeyError as e:
        logging.warning(f'응답 정보가 옳지 않습니다 응답 값: {e.args}')
        raise

    for v in variables['variables']:
        print(v)


if __name__ == "__main__":
    get_variables()
