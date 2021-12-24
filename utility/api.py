# -*- coding: utf-8 -*-
#
# Copyright (c) Sangsu Ryu

# === 표준 패키지 임포트 === #

from typing import Any

import json

# === 사용자 정의 모듈 임포트 === #

from constant.statusCode import STATUS_CODE

# === 함수 정의 === #

def makeResponse(status: str, data: Any) -> dict:
    '''
    JSON 형식의 응답 메시지를 생성합니다.

    Args:
        status (str): 상태 문자열
        data (Any): 응답 데이터

    Returns:
        response (dict): 응답 메시지
    '''

    status = status.upper()

    if status not in STATUS_CODE:
        status = 'STATUS_ERROR'
        data   = None

    return {
        'status': STATUS_CODE[status],
        'mimetype': 'application/json',
        'response': json.dumps({
            'status': status,
            'data': data
        })
    }