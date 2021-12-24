# -*- coding: utf-8 -*-
#
# Copyright (c) Sangsu Ryu

# === 표준 패키지 임포트 === #

from datetime import datetime

# === 서드파티 패키지 임포트 === #

from flask import Blueprint, Response, current_app, request

import psycopg2

# === 사용자 정의 모듈 임포트 === #

from constant.drug import DRUG, REVERSED_DRUG

import database.database as db
import utility.api       as api

# === 상수 정의 === #

DEFAULT_PAGE_SIZE = 10 # 페이지 당 출력 개수에 대한 기본 값

# === 전역 변수 정의 === #

blueprint = Blueprint('search_drug', __name__, url_prefix='/search/drug')

# === 라우터 정의 === #

@blueprint.route('/', methods=['GET'])
def index() -> Response:
    '''
    drug_exposure 테이블을 검색하기 위한 라우터입니다.

    Methods:
        GET

    Params:
        person_id (str, opt, default=None): 환자 ID 키워드
        visit_id (str, opt, default=None): 방문 ID 키워드
        drug (str, opt, default=None): 처방 의약품 키워드
        date (%Y-%m-%d~%Y-%m-%d, opt, default=None): 처방 기간 키워드
        page (str, opt, default=0): 페이지 번호
        page_size (str, opt, default=DEFAULT_PAGE_SIZE): 페이지 당 출력 개수

    Responses:
        {
            'status': <STATUS>,
            'data': {
                'drugs': [{
                    'person_id': <PERSON ID>,
                    'visit_id': <VISIT OCCURRENCE ID>,
                    'drug_concept_id': <DRUG CONCEPT ID>,
                    'drug_concept_name': <DRUG CONCEPT NAME>,
                    'start_date': <DRUG EXPOSURE START DATETIME>,
                    'end_date': <DRUG EXPOSURE END DATETIME>
                }, ...]
            }
        }
    '''

    # --- 파라미터 파싱 --- #

    parameter = request.args.to_dict()
    personID  = parameter.get('person_id', None)
    visitID   = parameter.get('visit_id', None)
    drug      = parameter.get('drug', None)
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
        'drugs': []
    }

    # --- 데이터베이스 조회 --- #

    try:
        with db.connection.cursor() as cursor:
            query = '''
                SELECT person_id, visit_occurrence_id, drug_concept_id, drug_exposure_start_datetime, drug_exposure_end_datetime
                FROM drug_exposure
            '''
            argument = []

            # --- 키워드 파싱을 통한 동적 쿼리 구성 --- #

            keywordNumber = sum([personID != None, visitID != None, drug != None, date != None])
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

            if drug != None:
                if keywordCount != 0:
                    query += ' AND'

                if drug in DRUG:
                    drugID = DRUG[drug]
                else:
                    drugID = None

                query        += ' drug_concept_id=%s'
                argument.append(drugID)
                keywordCount += 1

            if date != None:
                if keywordCount != 0:
                    query += ' AND'

                query        += ' drug_exposure_start_datetime >= %s AND drug_exposure_end_datetime <= %s'
                argument.extend([startDate, endDate])
                keywordCount += 1

            query += ' ORDER BY person_id OFFSET %s LIMIT %s'
            argument.extend([page, pageSize])

            cursor.execute(query, argument)

            for drug in cursor.fetchall():
                data['drugs'].append({
                    'person_id': drug['person_id'],
                    'visit_id': drug['visit_occurrence_id'],
                    'drug_concept_id': drug['drug_concept_id'],
                    'drug_concept_name': REVERSED_DRUG[drug['drug_concept_id']],
                    'start_date': drug['drug_exposure_start_datetime'].strftime('%Y-%m-%d'),
                    'end_date': drug['drug_exposure_end_datetime'].strftime('%Y-%m-%d')
                })
    except psycopg2.DatabaseError as error:
        status = 'DATABASE_ERROR'
        data   = None

        db.connection.rollback()
        current_app.logger.error(error)

    return Response(**api.makeResponse(status, data))