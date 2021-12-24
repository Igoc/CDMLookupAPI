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

DRUG          = {} # 처방 의약품 목록 (concept_name -> concept_id)
REVERSED_DRUG = {} # 처방 의약품 목록 (concept_id -> concept_name)

# === 함수 정의 === #

def refreshDrug() -> None:
    '''
    DRUG와 REVERSED_DRUG 값을 갱신합니다.
    '''

    try:
        with db.connection.cursor() as cursor:
            cursor.execute('''
                SELECT c.concept_id, c.concept_name
                FROM concept AS c JOIN (SELECT DISTINCT drug_concept_id FROM drug_exposure) as d
                ON c.concept_id=d.drug_concept_id AND c.domain_id=%s
            ''', ['Drug'])

            for concept in cursor.fetchall():
                DRUG[concept['concept_name']]        = concept['concept_id']
                REVERSED_DRUG[concept['concept_id']] = concept['concept_name']
    except psycopg2.DatabaseError as error:
        db.connection.rollback()
        sys.exit(error)