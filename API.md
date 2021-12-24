# CDM Lookup API 명세표

#### &nbsp; CDM Lookup API에 대한 명세표 <br/><br/>

## 통계 API

### 환자 수 조회 API

#### /statistic/person/person_count

##### 설명

전체 환자 수를 조회하기 위한 API

##### 메서드

GET

##### 응답 메시지

``` json
{
    "status": <STATUS>,
    "data": {
        "count": <COUNT>
    }
}
```

<br/>

#### /statistic/person/gender_count/\<gender>

##### 설명

성별 환자 수를 조회하기 위한 API

##### 메서드

GET

##### 응답 메시지

``` json
{
    "status": <STATUS>,
    "data": <GENDER> | {
        "count": <COUNT>
    }
}
```

<br/>

#### /statistic/person/race_count/\<race>

##### 설명

인종별 환자 수를 조회하기 위한 API

##### 메서드

GET

##### 응답 메시지

``` json
{
    "status": <STATUS>,
    "data": <RACE> | {
        "count": <COUNT>
    }
}
```

<br/>

#### /statistic/person/ethnicity_count/\<ethnicity>

##### 설명

민족별 환자 수를 조회하기 위한 API

##### 메서드

GET

##### 응답 메시지

``` json
{
    "status": <STATUS>,
    "data": <ETHNICITY> | {
        "count": <COUNT>
    }
}
```

<br/>

#### /statistic/person/death_count

##### 설명

사망 환자 수를 조회하기 위한 API

##### 메서드

GET

##### 응답 메시지

``` json
{
    "status": <STATUS>,
    "data": {
        "count": <COUNT>
    }
}
```

<br/>

### 방문 수 조회 API

#### /statistic/visit/visit_type_count/\<visitType>

##### 설명

방문 유형 별 방문 수를 조회하기 위한 API

##### 메서드

GET

##### 응답 메시지

``` json
{
    "status": <STATUS>,
    "data": <VISIT_TYPE> | {
        "count": <COUNT>
    }
}
```

<br/>

#### /statistic/visit/gender_count/\<gender>

##### 설명

성별 방문 수를 조회하기 위한 API

##### 메서드

GET

##### 응답 메시지

``` json
{
    "status": <STATUS>,
    "data": <GENDER> | {
        "count": <COUNT>
    }
}
```

<br/>

#### /statistic/visit/race_count/\<race>

##### 설명

인종별 방문 수를 조회하기 위한 API

##### 메서드

GET

##### 응답 메시지

``` json
{
    "status": <STATUS>,
    "data": <RACE> | {
        "count": <COUNT>
    }
}
```

<br/>

#### /statistic/visit/ethnicity_count/\<ethnicity>

##### 설명

민족별 방문 수를 조회하기 위한 API

##### 메서드

GET

##### 응답 메시지

``` json
{
    "status": <STATUS>,
    "data": <ETHNICITY> | {
        "count": <COUNT>
    }
}
```

<br/>

#### /statistic/visit/age_count/\<age>

##### 설명

10살 단위의 연령대별 방문 수를 조회하기 위한 API로, 만 나이를 기준으로 조회

##### 메서드

GET

##### 응답 메시지

``` json
{
    "status": <STATUS>,
    "data": [0, 10, 20, "..."] | {
        "count": <COUNT>
    }
}
```

<br/>

## 검색 API

### concept 테이블 검색 API

#### /search/concept

##### 설명

concept 테이블을 검색하기 위한 API로, 키워드가 있을 경우 concept_name을 대상으로 조회

##### 메서드

GET

##### 파라미터

- keyword (string, option): 검색 키워드
- page (string, option): 페이지 번호
- page_size (string, option): 페이지 당 출력 개수

##### 응답 메시지

``` json
{
    "status": <STATUS>,
    "data": {
        "concepts": [{
            "id": <CONCEPT ID>,
            "code": <CONCEPT CODE>,
            "name": <CONCEPT NAME>,
            "class": <CONCEPT CLASS ID>,
            "validity": "Valid" | "Invalid",
            "domain": <DOMAIN ID>,
            "vocabulary": <VOCABULARY ID>
        }, ...]
    }
}
```

<br/>

### condition_occurrence 테이블 검색 API

#### /search/condition

##### 설명

condition_occurrence 테이블을 검색하기 위한 API

##### 메서드

GET

##### 파라미터

- person_id (string, option): 환자 ID 키워드
- visit_id (string, option): 방문 ID 키워드
- condition (string, option): 진단병명 키워드
- date (%Y-%m-%d~%Y-%m-%d, option): 진단 기간 키워드
- page (string, option): 페이지 번호
- page_size (string, option): 페이지 당 출력 개수

##### 응답 메시지

``` json
{
    "status": <STATUS>,
    "data": {
        "conditions": [{
            "person_id": <PERSON ID>,
            "visit_id": <VISIT OCCURRENCE ID>,
            "condition_concept_id": <CONDITION CONCEPT ID>,
            "condition_concept_name": <CONDITION CONCEPT NAME>,
            "start_date": <CONDITION START DATETIME>,
            "end_date": <CONDITION END DATETIME>
        }, ...]
    }
}
```

<br/>

### death 테이블 검색 API

#### /search/death

##### 설명

death 테이블을 검색하기 위한 API

##### 메서드

GET

##### 파라미터

- person_id (string, option): 환자 ID 키워드
- date (%Y-%m-%d, option): 사망일 키워드
- page (string, option): 페이지 번호
- page_size (string, option): 페이지 당 출력 개수

##### 응답 메시지

``` json
{
    "status": <STATUS>,
    "data": {
        "death": [{
            "person_id": <PERSON ID>,
            "date": <DEATH DATE>
        }, ...]
    }
}
```

<br/>

### drug_exposure 테이블 검색 API

#### /search/drug

##### 설명

drug_exposure 테이블을 검색하기 위한 API

##### 메서드

GET

##### 파라미터

- person_id (string, option): 환자 ID 키워드
- visit_id (string, option): 방문 ID 키워드
- drug (string, option): 처방 의약품 키워드
- date (%Y-%m-%d~%Y-%m-%d, option): 처방 기간 키워드
- page (string, option): 페이지 번호
- page_size (string, option): 페이지 당 출력 개수

##### 응답 메시지

``` json
{
    "status": <STATUS>,
    "data": {
        "drugs": [{
            "person_id": <PERSON ID>,
            "visit_id": <VISIT OCCURRENCE ID>,
            "drug_concept_id": <DRUG CONCEPT ID>,
            "drug_concept_name": <DRUG CONCEPT NAME>,
            "start_date": <DRUG EXPOSURE START DATETIME>,
            "end_date": <DRUG EXPOSURE END DATETIME>
        }, ...]
    }
}
```

<br/>

### person 테이블 검색 API

#### /search/person

##### 설명

person 테이블을 검색하기 위한 API

##### 메서드

GET

##### 파라미터

- birth (%Y-%m-%d, option): 생년월일 키워드
- gender (string, option): 성별 키워드
- race (string, option): 인종 키워드
- ethnicity (string, option): 민족 키워드
- page (string, option): 페이지 번호
- page_size (string, option): 페이지 당 출력 개수

##### 응답 메시지

``` json
{
    "status": <STATUS>,
    "data": {
        "persons": [{
            "person_id": <PERSON ID>,
            "birth": <BIRTH DATETIME>,
            "gender_concept_id": <GENDER CONCEPT ID>,
            "gender_concept_name": <GENDER CONCEPT NAME>,
            "race_concept_id": <RACE CONCEPT ID>,
            "race_concept_name": <RACE CONCEPT NAME>,
            "ethnicity": <ETHNICITY SOURCE VALUE>
        }, ...]
    }
}
```

<br/>

### visit_occurrence 테이블 검색 API

#### /search/visit

##### 설명

visit_occurrence 테이블을 검색하기 위한 API

##### 메서드

GET

##### 파라미터

- person_id (string, option): 환자 ID 키워드
- visit_type (string, option): 방문 유형 키워드
- date (%Y-%m-%d~%Y-%m-%d, option): 방문 기간 키워드
- page (string, option): 페이지 번호
- page_size (string, option): 페이지 당 출력 개수

##### 응답 메시지

``` json
{
    "status": <STATUS>,
    "data": {
        "visits": [{
            "visit_id": <VISIT OCCURRENCE ID>,
            "person_id": <PERSON ID>,
            "visit_concept_id": <VISIT CONCEPT ID>,
            "visit_concept_name": <VISIT CONCEPT NAME>,
            "start_date": <VISIT START DATETIME>,
            "end_date": <VISIT END DATETIME>
        }, ...]
    }
}
```