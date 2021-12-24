# -*- coding: utf-8 -*-
#
# Copyright (c) Sangsu Ryu

# === 표준 패키지 임포트 === #

from datetime import datetime, time

# === 서드파티 패키지 임포트 === #

from flask import Blueprint, Response, current_app, request

import psycopg2

# === 사용자 정의 모듈 임포트 === #

import database.database as db
import utility.api       as api

# === 상수 정의 === #

DEFAULT_PAGE_SIZE = 10 # 페이지 당 출력 개수에 대한 기본 값

# === 전역 변수 정의 === #

blueprint = Blueprint('search_concept', __name__, url_prefix='/search/concept')

# === 라우터 정의 === #

@blueprint.route('/', methods=['GET'])
def index() -> Response:
    '''
    concept 테이블을 검색하기 위한 라우터로, 키워드가 있을 경우 concept_name을 대상으로 조회합니다.

    Methods:
        GET

    Params:
        keyword (str, opt, default=None): 검색 키워드
        page (str, opt, default=0): 페이지 번호
        page_size (str, opt, default=DEFAULT_PAGE_SIZE): 페이지 당 출력 개수

    Responses:
        {
            'status': <STATUS>,
            'data': {
                'concepts': [{
                    'id': <CONCEPT ID>,
                    'code': <CONCEPT CODE>,
                    'name': <CONCEPT NAME>,
                    'class': <CONCEPT CLASS ID>,
                    'validity': 'Valid' | 'Invalid',
                    'domain': <DOMAIN ID>,
                    'vocabulary': <VOCABULARY ID>
                }, ...]
            }
        }
    '''

    # --- 파라미터 파싱 --- #

    parameter = request.args.to_dict()
    keyword   = parameter.get('keyword', None)
    page      = parameter.get('page', 0)
    pageSize  = parameter.get('page_size', DEFAULT_PAGE_SIZE)

    page = str(int(page) * int(pageSize))

    # --- 응답 메시지 정의 --- #

    status = 'SUCCESS'
    data   = {
        'concepts': []
    }

    # --- 데이터베이스 조회 --- #

    try:
        with db.connection.cursor() as cursor:
            if keyword == None:
                cursor.execute('''
                    SELECT *
                    FROM concept
                    ORDER BY concept_id
                    OFFSET %s LIMIT %s
                ''', [page, pageSize])
            else:
                cursor.execute('''
                    SELECT *
                    FROM concept
                    WHERE concept_name LIKE %s
                    ORDER BY concept_id
                    OFFSET %s LIMIT %s
                ''', [f'%{keyword}%', page, pageSize])

            for concept in cursor.fetchall():
                data['concepts'].append({
                    'id': concept['concept_id'],
                    'code': concept['concept_code'],
                    'name': concept['concept_name'],
                    'class': concept['concept_class_id'],
                    'validity': 'Valid' if datetime.combine(concept['valid_end_date'], time(0, 0)) >= datetime.now() else 'Invalid',
                    'domain': concept['domain_id'],
                    'vocabulary': concept['vocabulary_id']
                })
    except psycopg2.DatabaseError as error:
        status = 'DATABASE_ERROR'
        data   = None

        db.connection.rollback()
        current_app.logger.error(error)

    return Response(**api.makeResponse(status, data))