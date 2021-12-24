# -*- coding: utf-8 -*-
#
# Copyright (c) Sangsu Ryu

# === 표준 패키지 임포트 === #

from datetime import datetime

# === 서드파티 패키지 임포트 === #

from dateutil.relativedelta import relativedelta
from flask                  import Blueprint, Response, current_app

import psycopg2

# === 사용자 정의 모듈 임포트 === #

from constant.ethnicity import ETHNICITY
from constant.gender    import GENDER
from constant.race      import RACE
from constant.visitType import VISIT_TYPE

import database.database as db
import utility.api       as api

# === 전역 변수 정의 === #

blueprint = Blueprint('statistic_visit', __name__, url_prefix='/statistic/visit')

# === 라우터 정의 === #

@blueprint.route('/visit_type_count', defaults={ 'visitType': None }, methods=['GET'])
@blueprint.route('/visit_type_count/<string:visitType>', methods=['GET'])
def visitTypeCount(visitType: str) -> Response:
    '''
    방문 유형 별 방문 수를 조회하기 위한 라우터입니다.

    Methods:
        GET

    Responses:
        {
            'status': <STATUS>,
            'data': <VISIT_TYPE> | {
                'count': <COUNT>
            }
        }
    '''

    # 테이블에 존재하지 않는 방문 유형을 조회할 경우, 조회 가능한 방문 유형을 반환합니다.
    if visitType not in VISIT_TYPE:
        return Response(**api.makeResponse('INVALID_DATA', list(VISIT_TYPE.keys())))

    # --- 응답 메시지 정의 --- #

    status = 'SUCCESS'
    data   = {
        'count': -1
    }

    # --- 데이터베이스 조회 --- #

    try:
        with db.connection.cursor() as cursor:
            cursor.execute('SELECT visit_occurrence_id FROM visit_occurrence WHERE visit_concept_id=%s', [VISIT_TYPE[visitType]])
            data['count'] = len(cursor.fetchall())
    except psycopg2.DatabaseError as error:
        status = 'DATABASE_ERROR'
        data   = None

        db.connection.rollback()
        current_app.logger.error(error)

    return Response(**api.makeResponse(status, data))

@blueprint.route('/gender_count', defaults={ 'gender': None }, methods=['GET'])
@blueprint.route('/gender_count/<string:gender>', methods=['GET'])
def genderCount(gender: str) -> Response:
    '''
    성별 방문 수를 조회하기 위한 라우터입니다.

    Methods:
        GET

    Responses:
        {
            'status': <STATUS>,
            'data': <GENDER> | {
                'count': <COUNT>
            }
        }
    '''

    # 테이블에 존재하지 않는 성별을 조회할 경우, 조회 가능한 성별 목록을 반환합니다.
    if gender not in GENDER:
        return Response(**api.makeResponse('INVALID_DATA', list(GENDER.keys())))

    # --- 응답 메시지 정의 --- #

    status = 'SUCCESS'
    data   = {
        'count': -1
    }

    # --- 데이터베이스 조회 --- #

    try:
        with db.connection.cursor() as cursor:
            cursor.execute('''
                SELECT v.visit_occurrence_id
                FROM person AS p JOIN visit_occurrence AS v
                ON p.person_id=v.person_id AND p.gender_concept_id=%s
            ''', [GENDER[gender]])
            data['count'] = len(cursor.fetchall())
    except psycopg2.DatabaseError as error:
        status = 'DATABASE_ERROR'
        data   = None

        db.connection.rollback()
        current_app.logger.error(error)

    return Response(**api.makeResponse(status, data))

@blueprint.route('/race_count', defaults={ 'race': None }, methods=['GET'])
@blueprint.route('/race_count/<string:race>', methods=['GET'])
def raceCount(race: str) -> Response:
    '''
    인종별 방문 수를 조회하기 위한 라우터입니다.

    Methods:
        GET

    Responses:
        {
            'status': <STATUS>,
            'data': <RACE> | {
                'count': <COUNT>
            }
        }
    '''

    # 테이블에 존재하지 않는 인종을 조회할 경우, 조회 가능한 인종 목록을 반환합니다.
    if race not in RACE:
        return Response(**api.makeResponse('INVALID_DATA', list(RACE.keys())))

    # --- 응답 메시지 정의 --- #

    status = 'SUCCESS'
    data   = {
        'count': -1
    }

    # --- 데이터베이스 조회 --- #

    try:
        with db.connection.cursor() as cursor:
            cursor.execute('''
                SELECT v.visit_occurrence_id
                FROM person AS p JOIN visit_occurrence AS v
                ON p.person_id=v.person_id AND p.race_concept_id=%s
            ''', [RACE[race]])
            data['count'] = len(cursor.fetchall())
    except psycopg2.DatabaseError as error:
        status = 'DATABASE_ERROR'
        data   = None

        db.connection.rollback()
        current_app.logger.error(error)

    return Response(**api.makeResponse(status, data))

@blueprint.route('/ethnicity_count', defaults={ 'ethnicity': None }, methods=['GET'])
@blueprint.route('/ethnicity_count/<string:ethnicity>', methods=['GET'])
def ethnicityCount(ethnicity: str) -> Response:
    '''
    민족별 방문 수를 조회하기 위한 라우터입니다.

    Methods:
        GET

    Responses:
        {
            'status': <STATUS>,
            'data': <ETHNICITY> | {
                'count': <COUNT>
            }
        }
    '''

    # 테이블에 존재하지 않는 민족을 조회할 경우, 조회 가능한 민족 목록을 반환합니다.
    if ethnicity not in ETHNICITY:
        return Response(**api.makeResponse('INVALID_DATA', list(ETHNICITY)))

    # --- 응답 메시지 정의 --- #

    status = 'SUCCESS'
    data   = {
        'count': -1
    }

    # --- 데이터베이스 조회 --- #

    try:
        with db.connection.cursor() as cursor:
            cursor.execute('''
                SELECT v.visit_occurrence_id
                FROM person AS p JOIN visit_occurrence AS v
                ON p.person_id=v.person_id AND p.ethnicity_source_value=%s
            ''', [ethnicity])
            data['count'] = len(cursor.fetchall())
    except psycopg2.DatabaseError as error:
        status = 'DATABASE_ERROR'
        data   = None

        db.connection.rollback()
        current_app.logger.error(error)

    return Response(**api.makeResponse(status, data))

@blueprint.route('/age_count', defaults={ 'age': None }, methods=['GET'])
@blueprint.route('/age_count/<int:age>', methods=['GET'])
def ageCount(age: int) -> Response:
    '''
    10살 단위의 연령대별 방문 수를 조회하기 위한 라우터로, 만 나이를 기준으로 합니다.

    Methods:
        GET

    Responses:
        {
            'status': <STATUS>,
            'data': [0, 10, 20, '...'] | {
                'count': <COUNT>
            }
        }
    '''

    # 10살 단위의 조회가 아닐 경우, 올바른 조회 방법을 반환합니다.
    if age == None or age % 10 != 0:
        return Response(**api.makeResponse('INVALID_DATA', [0, 10, 20, '...']))

    # --- 응답 메시지 정의 --- #

    status = 'SUCCESS'
    data   = {
        'count': -1
    }

    # --- 만 나이를 기준으로 생년월일 범위 산출 --- #

    offset    = age // 10
    startDate = datetime.now() - relativedelta(years=10 * (offset + 1)) + relativedelta(days=1)
    endDate   = datetime.now() - relativedelta(years=10 * offset)

    startDate = datetime(startDate.year, startDate.month, startDate.day)
    endDate   = datetime(endDate.year, endDate.month, endDate.day, 23, 59, 59)

    # --- 데이터베이스 조회 --- #

    try:
        with db.connection.cursor() as cursor:
            cursor.execute('''
                SELECT v.visit_occurrence_id
                FROM person AS p JOIN visit_occurrence AS v
                ON p.person_id=v.person_id AND (p.birth_datetime BETWEEN %s AND %s)
            ''', [startDate, endDate])
            data['count'] = len(cursor.fetchall())
    except psycopg2.DatabaseError as error:
        status = 'DATABASE_ERROR'
        data   = None

        db.connection.rollback()
        current_app.logger.error(error)

    return Response(**api.makeResponse(status, data))