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

VISIT_TYPE          = {} # 방문 유형 목록 (concept_name -> concept_id)
REVERSED_VISIT_TYPE = {} # 방문 유형 목록 (concept_id -> concept_name)

# === 함수 정의 === #

def refreshVisitType() -> None:
    '''
    VISIT_TYPE과 REVERSED_VISIT_TYPE 값을 갱신합니다.
    '''

    try:
        with db.connection.cursor() as cursor:
            cursor.execute('''
                SELECT c.concept_id, c.concept_name
                FROM concept AS c JOIN (SELECT DISTINCT visit_concept_id FROM visit_occurrence) AS v
                ON c.concept_id=v.visit_concept_id AND c.domain_id=%s
            ''', ['Visit'])

            for concept in cursor.fetchall():
                VISIT_TYPE[concept['concept_name']]        = concept['concept_id']
                REVERSED_VISIT_TYPE[concept['concept_id']] = concept['concept_name']
    except psycopg2.DatabaseError as error:
        db.connection.rollback()
        sys.exit(error)