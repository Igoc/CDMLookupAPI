# -*- coding: utf-8 -*-
#
# Copyright (c) Sangsu Ryu

# === 표준 패키지 임포트 === #

from datetime import datetime

# === 서드파티 패키지 임포트 === #

from flask import Blueprint, Response, current_app, request

import psycopg2

# === 사용자 정의 모듈 임포트 === #

from constant.ethnicity import ETHNICITY
from constant.gender    import GENDER, REVERSED_GENDER
from constant.race      import RACE, REVERSED_RACE

import database.database as db
import utility.api       as api

# === 상수 정의 === #

DEFAULT_PAGE_SIZE = 10 # 페이지 당 출력 개수에 대한 기본 값

# === 전역 변수 정의 === #

blueprint = Blueprint('search_person', __name__, url_prefix='/search/person')

# === 라우터 정의 === #

@blueprint.route('/', methods=['GET'])
def index() -> Response:
    '''
    person 테이블을 검색하기 위한 라우터입니다.

    Methods:
        GET

    Params:
        birth (%Y-%m-%d, opt, default=None): 생년월일 키워드
        gender (str, opt, default=None): 성별 키워드
        race (str, opt, default=None): 인종 키워드
        ethnicity (str, opt, default=None): 민족 키워드
        page (str, opt, default=0): 페이지 번호
        page_size (str, opt, default=DEFAULT_PAGE_SIZE): 페이지 당 출력 개수

    Responses:
        {
            'status': <STATUS>,
            'data': {
                'persons': [{
                    'person_id': <PERSON ID>,
                    'birth': <BIRTH DATETIME>,
                    'gender_concept_id': <GENDER CONCEPT ID>,
                    'gender_concept_name': <GENDER CONCEPT NAME>,
                    'race_concept_id': <RACE CONCEPT ID>,
                    'race_concept_name': <RACE CONCEPT NAME>,
                    'ethnicity': <ETHNICITY SOURCE VALUE>
                }, ...]
            }
        }
    '''

    # --- 파라미터 파싱 --- #

    parameter = request.args.to_dict()
    birth     = parameter.get('birth', None)
    gender    = parameter.get('gender', None)
    race      = parameter.get('race', None)
    ethnicity = parameter.get('ethnicity', None)
    page      = parameter.get('page', 0)
    pageSize  = parameter.get('page_size', DEFAULT_PAGE_SIZE)

    if birth != None:
        birth = birth.split('-')
        birth = datetime(int(birth[0]), int(birth[1]), int(birth[2]))

    page = str(int(page) * int(pageSize))

    # --- 응답 메시지 정의 --- #

    status = 'SUCCESS'
    data   = {
        'persons': []
    }

    # --- 데이터베이스 조회 --- #

    try:
        with db.connection.cursor() as cursor:
            query = '''
                SELECT person_id, birth_datetime, gender_concept_id, race_concept_id, ethnicity_source_value
                FROM person
            '''
            argument = []

            # --- 키워드 파싱을 통한 동적 쿼리 구성 --- #

            keywordNumber = sum([birth != None, gender != None, race != None, ethnicity != None])
            keywordCount  = 0

            if keywordNumber != 0:
                query += ' WHERE'

            if birth != None:
                if keywordCount != 0:
                    query += ' AND'

                query        += ' birth_datetime=%s'
                argument.append(birth)
                keywordCount += 1

            if gender != None:
                if keywordCount != 0:
                    query += ' AND'

                if gender in GENDER:
                    genderID = GENDER[gender]
                else:
                    genderID = None

                query        += ' gender_concept_id=%s'
                argument.append(genderID)
                keywordCount += 1

            if race != None:
                if keywordCount != 0:
                    query += ' AND'

                if race in RACE:
                    raceID = RACE[race]
                else:
                    raceID = None

                query        += ' race_concept_id=%s'
                argument.append(raceID)
                keywordCount += 1

            if ethnicity != None:
                if keywordCount != 0:
                    query += ' AND'

                if ethnicity not in ETHNICITY:
                    ethnicity = None

                query        += ' ethnicity_source_value=%s'
                argument.append(ethnicity)
                keywordCount += 1

            query += ' ORDER BY person_id OFFSET %s LIMIT %s'
            argument.extend([page, pageSize])

            cursor.execute(query, argument)

            for person in cursor.fetchall():
                data['persons'].append({
                    'person_id': person['person_id'],
                    'birth': person['birth_datetime'].strftime('%Y-%m-%d'),
                    'gender_concept_id': person['gender_concept_id'],
                    'gender_concept_name': REVERSED_GENDER[person['gender_concept_id']],
                    'race_concept_id': person['race_concept_id'],
                    'race_concept_name': REVERSED_RACE[person['race_concept_id']],
                    'ethnicity': person['ethnicity_source_value']
                })
    except psycopg2.DatabaseError as error:
        status = 'DATABASE_ERROR'
        data   = None

        db.connection.rollback()
        current_app.logger.error(error)

    return Response(**api.makeResponse(status, data))