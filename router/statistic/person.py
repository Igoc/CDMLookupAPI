# -*- coding: utf-8 -*-
#
# Copyright (c) Sangsu Ryu

# === 서드파티 패키지 임포트 === #

from flask import Blueprint, Response, current_app

import psycopg2

# === 사용자 정의 모듈 임포트 === #

from constant.ethnicity import ETHNICITY
from constant.gender    import GENDER
from constant.race      import RACE

import database.database as db
import utility.api       as api

# === 전역 변수 정의 === #

blueprint = Blueprint('statistic_person', __name__, url_prefix='/statistic/person')

# === 라우터 정의 === #

@blueprint.route('/person_count', methods=['GET'])
def personCount() -> Response:
    '''
    전체 환자 수를 조회하기 위한 라우터입니다.

    Methods:
        GET

    Responses:
        {
            'status': <STATUS>,
            'data': {
                'count': <COUNT>
            }
        }
    '''

    # --- 응답 메시지 정의 --- #

    status = 'SUCCESS'
    data   = {
        'count': -1
    }

    # --- 데이터베이스 조회 --- #

    try:
        with db.connection.cursor() as cursor:
            cursor.execute('SELECT person_id FROM person')
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
    성별 환자 수를 조회하기 위한 라우터입니다.

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
            cursor.execute('SELECT person_id FROM person WHERE gender_concept_id=%s', [GENDER[gender]])
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
    인종별 환자 수를 조회하기 위한 라우터입니다.

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
            cursor.execute('SELECT person_id FROM person WHERE race_concept_id=%s', [RACE[race]])
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
    민족별 환자 수를 조회하기 위한 라우터입니다.

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
            cursor.execute('SELECT person_id FROM person WHERE ethnicity_source_value=%s', [ethnicity])
            data['count'] = len(cursor.fetchall())
    except psycopg2.DatabaseError as error:
        status = 'DATABASE_ERROR'
        data   = None

        db.connection.rollback()
        current_app.logger.error(error)

    return Response(**api.makeResponse(status, data))

@blueprint.route('/death_count', methods=['GET'])
def deathCount() -> Response:
    '''
    사망 환자 수를 조회하기 위한 라우터입니다.

    Methods:
        GET

    Responses:
        {
            'status': <STATUS>,
            'data': {
                'count': <COUNT>
            }
        }
    '''

    # --- 응답 메시지 정의 --- #

    status = 'SUCCESS'
    data   = {
        'count': -1
    }

    # --- 데이터베이스 조회 --- #

    try:
        with db.connection.cursor() as cursor:
            cursor.execute('SELECT person_id FROM death')
            data['count'] = len(cursor.fetchall())
    except psycopg2.DatabaseError as error:
        status = 'DATABASE_ERROR'
        data   = None

        db.connection.rollback()
        current_app.logger.error(error)

    return Response(**api.makeResponse(status, data))