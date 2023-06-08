1. DAGs 폴더는 어디에 지정되는가?   
   -> `dags_folder`
2. DAGs 폴더에 새로운 Dag를 만들면 언제 실제로 Airflow 시스템에서 이를 알게
   되나? 이 스캔 주기를 결정해주는 키의 이름이 무엇인가?  
   -> 주기적으로 5분마다 스캔한다, `dag_dir_list_interval`
3. 이 파일에서 Airflow를 API 형태로 외부에서 조작하고 싶다면 어느 섹션을
   변경해야하는가?  
   -> `api` 섹션
4. Variable에서 변수의 값이 encrypted가 되려면 변수의 이름에 어떤 단어들이
   들어가야 하는데 이 단어들은 무엇일까? :)  
   -> password, secret, passwd, authorization, api_key, apikey, access_token
5. 이 환경 설정 파일이 수정되었다면 이를 실제로 반영하기 위해서 해야 하는
   일은?  
   -> 서비스 재실행
   ```
   sudo systemctl restart airflow-scheduler
   sudo systemctl restart airflow-webserver
   ```ㅁ

6. Metadata DB의 내용을 암호화하는데 사용되는 키는 무엇인가?    
   -> `fernet_key`