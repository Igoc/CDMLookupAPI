# -*- coding: utf-8 -*-
#
# Copyright (c) Sangsu Ryu

# === 표준 패키지 임포트 === #

import os

# === 서드파티 패키지 임포트 === #

import psycopg2.extras

# === 전역 변수 정의 === #

config = {
    'host': os.getenv('CDM_LOOKUP_DATABASE_HOST'),
    'port': os.getenv('CDM_LOOKUP_DATABASE_PORT'),

    'user': os.getenv('CDM_LOOKUP_DATABASE_USER'),
    'password': os.getenv('CDM_LOOKUP_DATABASE_PASSWORD'),

    'dbname': os.getenv('CDM_LOOKUP_DATABASE_NAME'),
    'cursor_factory': psycopg2.extras.RealDictCursor
}