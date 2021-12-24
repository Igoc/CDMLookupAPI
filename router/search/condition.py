# -*- coding: utf-8 -*-
#
# Copyright (c) Sangsu Ryu

# === 표준 패키지 임포트 === #

from datetime import datetime

# === 서드파티 패키지 임포트 === #

from flask import Blueprint, Response, current_app, request

import psycopg2

# === 사용자 정의 모듈 임포트 === #

from constant.condition import CONDITION, REVERSED_CONDITION

import database.database as db
import utility.api       as api

# === 상수 정의 === #

DEFAULT_PAGE_SIZE = 10 # 페이지 당 출력 개수에 대한 기본 값

# === 전역 변수 정의 === #

blueprint = Blueprint('search_condition', __name__, url_prefix='/search/condition')

# === 라우터 정의 === #

@blueprint.route('/', methods=['GET'])
def index() -> Response:
    '''
    condition_occurrence 테이블을 검색하기 위한 라우터입니다.

    Methods:
        GET

    Params:
        person_id (str, opt, default=None): 환자 ID 키워드
        visit_id (str, opt, default=None): 방문 ID 키워드
        condition (str, opt, default=None): 진단병명 키워드
        date (%Y-%m-%d~%Y-%m-%d, opt, default=None): 진단 기간 키워드
        page (str, opt, default=0): 페이지 번호
        page_size (str, opt, default=DEFAULT_PAGE_SIZE): 페이지 당 출력 개수

    Responses:
        {
            'status': <STATUS>,
            'data': {
                'conditions': [{
                    'person_id': <PERSON ID>,
                    'visit_id': <VISIT OCCURRENCE ID>,
                    'condition_concept_id': <CONDITION CONCEPT ID>,
                    'condition_concept_name': <CONDITION CONCEPT NAME>,
                    'start_date': <CONDITION START DATETIME>,
                    'end_date': <CONDITION END DATETIME>
                }, ...]
            }
        }
    '''

    # --- 파라미터 파싱 --- #

    parameter = request.args.to_dict()
    personID  = parameter.get('person_id', None)
    visitID   = parameter.get('visit_id', None)
    condition = parameter.get('condition', None)
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
        'conditions': []
    }

    # --- 데이터베이스 조회 --- #

    try:
        with db.connection.cursor() as cursor:
            query = '''
                SELECT person_id, visit_occurrence_id, condition_concept_id, condition_start_datetime, condition_end_datetime
                FROM condition_occurrence
            '''
            argument = []

            # --- 키워드 파싱을 통한 동적 쿼리 구성 --- #

            keywordNumber = sum([personID != None, visitID != None, condition != None, date != None])
            keywordCount  = 0

            if keywordNumber != 0:
                query += ' WHERE'

            if personID != None:
                if keywordCount != 0:
                    query += ' AND'

                query        += ' person_id=%s'
                argument.append(personID)
                keywordCount += 1

            if visitID != None:
                if keywordCount != 0:
                    query += ' AND'

                query        += ' visit_occurrence_id=%s'
                argument.append(visitID)
                keywordCount += 1

            if condition != None:
                if keywordCount != 0:
                    query += ' AND'

                if condition in CONDITION:
                    conditionID = CONDITION[condition]
                else:
                    conditionID = None

                query        += ' condition_concept_id=%s'
                argument.append(conditionID)
                keywordCount += 1

            if date != None:
                if keywordCount != 0:
                    query += ' AND'

                query        += ' condition_start_datetime >= %s AND condition_end_datetime <= %s'
                argument.extend([startDate, endDate])
                keywordCount += 1

            query += ' ORDER BY person_id OFFSET %s LIMIT %s'
            argument.extend([page, pageSize])

            cursor.execute(query, argument)

            for condition in cursor.fetchall():
                data['conditions'].append({
                    'person_id': condition['person_id'],
                    'visit_id': condition['visit_occurrence_id'],
                    'condition_concept_id': condition['condition_concept_id'],
                    'condition_concept_name': None if condition['condition_concept_id'] == 0 else REVERSED_CONDITION[condition['condition_concept_id']],
                    'start_date': condition['condition_start_datetime'].strftime('%Y-%m-%d'),
                    'end_date': None if condition['condition_end_datetime'] == None else condition['condition_end_datetime'].strftime('%Y-%m-%d')
                })
    except psycopg2.DatabaseError as error:
        status = 'DATABASE_ERROR'
        data   = None

        db.connection.rollback()
        current_app.logger.error(error)

    return Response(**api.makeResponse(status, data))