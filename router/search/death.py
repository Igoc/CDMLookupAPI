# -*- coding: utf-8 -*-
#
# Copyright (c) Sangsu Ryu

# === 표준 패키지 임포트 === #

from datetime import date as dt

# === 서드파티 패키지 임포트 === #

from flask import Blueprint, Response, current_app, request

import psycopg2

# === 사용자 정의 모듈 임포트 === #

import database.database as db
import utility.api       as api

# === 상수 정의 === #

DEFAULT_PAGE_SIZE = 10 # 페이지 당 출력 개수에 대한 기본 값

# === 전역 변수 정의 === #

blueprint = Blueprint('search_death', __name__, url_prefix='/search/death')

# === 라우터 정의 === #

@blueprint.route('/', methods=['GET'])
def index() -> Response:
    '''
    death 테이블을 검색하기 위한 라우터입니다.

    Methods:
        GET

    Params:
        person_id (str, opt, default=None): 환자 ID 키워드
        date (%Y-%m-%d, opt, default=None): 사망일 키워드
        page (str, opt, default=0): 페이지 번호
        page_size (str, opt, default=DEFAULT_PAGE_SIZE): 페이지 당 출력 개수

    Responses:
        {
            'status': <STATUS>,
            'data': {
                'death': [{
                    'person_id': <PERSON ID>,
                    'date': <DEATH DATE>
                }, ...]
            }
        }
    '''

    # --- 파라미터 파싱 --- #

    parameter = request.args.to_dict()
    personID  = parameter.get('person_id', None)
    date      = parameter.get('date', None)
    page      = parameter.get('page', 0)
    pageSize  = parameter.get('page_size', DEFAULT_PAGE_SIZE)

    if date != None:
        date = date.split('-')
        date = dt(int(date[0]), int(date[1]), int(date[2]))

    page = str(int(page) * int(pageSize))

    # --- 응답 메시지 정의 --- #

    status = 'SUCCESS'
    data   = {
        'death': []
    }

    # --- 데이터베이스 조회 --- #

    try:
        with db.connection.cursor() as cursor:
            query = '''
                SELECT person_id, death_date
                FROM death
            '''
            argument = []

            # --- 키워드 파싱을 통한 동적 쿼리 구성 --- #

            keywordNumber = sum([personID != None, date != None])
            keywordCount  = 0

            if keywordNumber != 0:
                query += ' WHERE'

            if personID != None:
                if keywordCount != 0:
                    query += ' AND'

                query        += ' person_id=%s'
                argument.append(personID)
                keywordCount += 1

            if date != None:
                if keywordCount != 0:
                    query += ' AND'

                query        += ' death_date=%s'
                argument.append(date)
                keywordCount += 1

            query += ' ORDER BY person_id OFFSET %s LIMIT %s'
            argument.extend([page, pageSize])

            cursor.execute(query, argument)

            for death in cursor.fetchall():
                data['death'].append({
                    'person_id': death['person_id'],
                    'date': death['death_date'].strftime('%Y-%m-%d')
                })
    except psycopg2.DatabaseError as error:
        status = 'DATABASE_ERROR'
        data   = None

        db.connection.rollback()
        current_app.logger.error(error)

    return Response(**api.makeResponse(status, data))