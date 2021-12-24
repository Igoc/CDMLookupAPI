# -*- coding: utf-8 -*-
#
# Copyright (c) Sangsu Ryu

# === 표준 패키지 임포트 === #

import sys

# === 서드파티 패키지 임포트 === #

import psycopg2

# === 사용자 정의 모듈 임포트 === #

import database.database as db

# === 상수 정의 === #

ETHNICITY = set() # 민족 목록

# === 함수 정의 === #

def refreshEthnicity() -> None:
    '''
    ETHNICITY 값을 갱신합니다.
    '''

    try:
        with db.connection.cursor() as cursor:
            # 유효한 ethnicity_concept_id가 존재하지 않아, ethnicity_source_value로 대체
            cursor.execute('SELECT DISTINCT ethnicity_source_value FROM person')

            for person in cursor.fetchall():
                ETHNICITY.add(person['ethnicity_source_value'])
    except psycopg2.DatabaseError as error:
        db.connection.rollback()
        sys.exit(error)