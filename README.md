# CDM Lookup API

#### &nbsp; [Common Data Model](https://ohdsi.github.io/CommonDataModel/)을 조회하기 위한 API

&nbsp; API 명세표는 [API.md](https://github.com/Igoc/CDMLookupAPI/blob/main/API.md)에 정의되어 있습니다. <br/><br/>

## 사전 조건

### Python

&nbsp; Python 3.8 이상의 버전이 요구되며, 사용되는 의존성 패키지 목록은 [requirements.txt](https://github.com/Igoc/CDMLookupAPI/blob/main/requirements.txt)에 명시되어 있습니다.

``` bash
# 의존성 패키지 설치
pip install -r requirements.txt
```

<br/>

### 환경 변수

&nbsp; Flask 애플리케이션 구동을 위해, 다음과 같은 환경 변수 설정이 필요합니다.

``` bash
# Flask 애플리케이션 환경 변수
export CDM_LOOKUP_SECRET_KEY="<FLASK SECRET KEY>"

# PostgreSQL 환경 변수
export CDM_LOOKUP_DATABASE_HOST="<POSTGRESQL HOST>"
export CDM_LOOKUP_DATABASE_PORT="<POSTGRESQL PORT>"

export CDM_LOOKUP_DATABASE_USER="<POSTGRESQL USER>"
export CDM_LOOKUP_DATABASE_PASSWORD="<POSTGRESQL PASSWORD>"

export CDM_LOOKUP_DATABASE_NAME="<POSTGRESQL DATABASE>"
```

<br/>

## 사용법

``` bash
# 개발 서버 실행
python application.py

# 프로덕션 서버 실행
uwsgi --ini uWSGI.ini
```