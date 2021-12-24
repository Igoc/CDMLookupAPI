# -*- coding: utf-8 -*-
#
# Copyright (c) Sangsu Ryu

# === 표준 패키지 임포트 === #

from datetime import datetime

# === 서드파티 패키지 임포트 === #

from flask import Blueprint, Response, current_app, request

import psycopg2

# === 사용자 정의 모듈 임포트 === #

from constant.visitType import VISIT_TYPE, REVERSED_VISIT_TYPE

import database.database as db
import utility.api       as api

# === 상수 정의 === #

DEFAULT_PAGE_SIZE = 10 # 페이지 당 출력 개수에 대한 기본 값

# === 전역 변수 정의 === #

blueprint = Blueprint('search_visit', __name__, url_prefix='/search/visit')

# === 라우터 정의 === #

@blueprint.route('/', methods=['GET'])
def index() -> Response:
    '''
    visit_occurrence 테이블을 검색하기 위한 라우터입니다.

    Methods:
        GET

    Params:
        person_id (str, opt, default=None): 환자 ID 키워드
        visit_type (str, opt, default=None): 방문 유형 키워드
        date (%Y-%m-%d~%Y-%m-%d, opt, default=None): 방문 기간 키워드
        page (str, opt, default=0): 페이지 번호
        page_size (str, opt, default=DEFAULT_PAGE_SIZE): 페이지 당 출력 개수

    Responses:
        {
            'status': <STATUS>,
            'data': {
                'visits': [{
                    'visit_id': <VISIT OCCURRENCE ID>,
                    'person_id': <PERSON ID>,
                    'visit_concept_id': <VISIT CONCEPT ID>,
                    'visit_concept_name': <VISIT CONCEPT NAME>,
                    'start_date': <VISIT START DATETIME>,
                    'end_date': <VISIT END DATETIME>
                }, ...]
            }
        }
    '''

    # --- 파라미터 파싱 --- #

    parameter = request.args.to_dict()
    personID  = parameter.get('person_id', None)
    visitType = parameter.get('visit_type', None)
    date      = parameter.get('date', None)
    page      = parameter.get('page', 0)
    pageSize  = parameter.get('page_size', DEFAULT_PAGE_SIZE)

    if date != None:
        date = date.split('~')

        startDate = date[0].split('-')
        startDate = datetime(int(startDate[0]), int(startDate[1]), int(startDate[2]))

        endDate = date[1].split('-')
        endDate = datetime(int(endDate[0]), int(endDate[1]), int(endDate[2]))

    page = str(int(page) * int(pageSize))

    # --- 응답 메시지 정의 --- #

    status = 'SUCCESS'
    data   = {
        'visits': []
    }

    # --- 데이터베이스 조회 --- #

    try:
        with db.connection.cursor() as cursor:
            query = '''
                SELECT visit_occurrence_id, person_id, visit_concept_id, visit_start_datetime, visit_end_datetime
                FROM visit_occurrence
            '''
            argument = []

            # --- 키워드 파싱을 통한 동적 쿼리 구성 --- #

            keywordNumber = sum([personID != None, visitType != None, date != None])
            keywordCount  = 0

            if keywordNumber != 0:
                query += ' WHERE'

            if personID != None:
                if keywordCount != 0:
                    query += ' AND'

                query        += ' person_id=%s'
                argument.append(personID)
                keywordCount += 1

            if visitType != None:
                if keywordCount != 0:
                    query += ' AND'

                if visitType in VISIT_TYPE:
                    visitTypeID = VISIT_TYPE[visitType]
                else:
                    visitTypeID = None

                query        += ' visit_concept_id=%s'
                argument.append(visitTypeID)
                keywordCount += 1

            if date != None:
                if keywordCount != 0:
                    query += ' AND'

                query        += ' visit_start_datetime >= %s AND visit_end_datetime <= %s'
                argument.extend([startDate, endDate])
                keywordCount += 1

            query += ' ORDER BY visit_occurrence_id OFFSET %s LIMIT %s'
            argument.extend([page, pageSize])

            cursor.execute(query, argument)

            for visit in cursor.fetchall():
                data['visits'].append({
                    'visit_id': visit['visit_occurrence_id'],
                    'person_id': visit['person_id'],
                    'visit_concept_id': visit['visit_concept_id'],
                    'visit_concept_name': REVERSED_VISIT_TYPE[visit['visit_concept_id']],
                    'start_date': visit['visit_start_datetime'].strftime('%Y-%m-%d'),
                    'end_date': visit['visit_end_datetime'].strftime('%Y-%m-%d')
                })
    except psycopg2.DatabaseError as error:
        status = 'DATABASE_ERROR'
        data   = None

        db.connection.rollback()
        current_app.logger.error(error)

    return Response(**api.makeResponse(status, data))