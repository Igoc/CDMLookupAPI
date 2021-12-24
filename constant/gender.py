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

GENDER          = {} # 성별 목록 (concept_name -> concept_id)
REVERSED_GENDER = {} # 성별 목록 (concept_id -> concept_name)

# === 함수 정의 === #

def refreshGender() -> None:
    '''
    GENDER와 REVERSED_GENDER 값을 갱신합니다.
    '''

    try:
        with db.connection.cursor() as cursor:
            cursor.execute('''
                SELECT c.concept_id, c.concept_name
                FROM concept AS c JOIN (SELECT DISTINCT gender_concept_id FROM person) AS p
                ON c.concept_id=p.gender_concept_id AND c.domain_id=%s
            ''', ['Gender'])

            for concept in cursor.fetchall():
                GENDER[concept['concept_name']]        = concept['concept_id']
                REVERSED_GENDER[concept['concept_id']] = concept['concept_name']
    except psycopg2.DatabaseError as error:
        db.connection.rollback()
        sys.exit(error)