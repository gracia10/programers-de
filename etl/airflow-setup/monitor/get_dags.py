import logging

import requests
from requests import HTTPError, JSONDecodeError
from requests.auth import HTTPBasicAuth

url = "http://localhost:8080/api/v1/dags"


def get_unpaused_dags():
    """
        활성화된 DAG 만 조회하는 함수
        - Airflow 2.6.0 부터 API Query Param 으로 조회할 수 있다 (paused)
    """
    res = requests.get(url, auth=HTTPBasicAuth("airflow", "airflow"))

    # http 통신 응답값 검증
    try:
        res.raise_for_status()
        dags = res.json()
        if dags.get('dags') is None:
            raise KeyError(dags)
    except (HTTPError, JSONDecodeError) as e:
        logging.warning(f'오류가 발생했습니다. 상태 코드: {e.response.status_code}')
        raise
    except KeyError as e:
        logging.warning(f'응답 정보가 옳지 않습니다 응답 값: {e.args}')
        raise

    # 활성화된 dag 조회
    paused_false_dags = [dag for dag in dags['dags'] if not dag['is_paused']]

    for dag in paused_false_dags:
        print(dag)


if __name__ == "__main__":
    get_unpaused_dags()
