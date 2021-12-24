# -*- coding: utf-8 -*-
#
# Copyright (c) Sangsu Ryu

# === 서드파티 패키지 임포트 === #

import psycopg2

# === 사용자 정의 모듈 임포트 === #

import config.database

# === 전역 변수 정의 === #

connection = psycopg2.connect(**config.database.config)