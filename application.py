# -*- coding: utf-8 -*-
#
# Copyright (c) Sangsu Ryu

# === 표준 패키지 임포트 === #

from typing import Any

import atexit
import datetime
import logging
import os

# === 서드파티 패키지 임포트 === #

from apscheduler.schedulers.background import BackgroundScheduler
from flask                             import Flask, request
from flask.logging                     import default_handler

# === 사용자 정의 모듈 임포트 === #

from constant.condition import refreshCondition
from constant.drug      import refreshDrug
from constant.ethnicity import refreshEthnicity
from constant.gender    import refreshGender
from constant.race      import refreshRace
from constant.visitType import refreshVisitType
from router.search      import concept          as search_concept
from router.search      import condition        as search_condition
from router.search      import death            as search_death
from router.search      import drug             as search_drug
from router.search      import person           as search_person
from router.search      import visit            as search_visit
from router.statistic   import person           as statistic_person
from router.statistic   import visit            as statistic_visit

# === 로거 설정 === #

default_handler.setFormatter('')
logging.getLogger('werkzeug').setLevel(logging.ERROR)

# === Flask 애플리케이션 정의 === #

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
app.config.update(
    DEBUG=True,
    SECRET_KEY=os.getenv('CDM_LOOKUP_SECRET_KEY')
)

app.register_blueprint(search_concept.blueprint)
app.register_blueprint(search_condition.blueprint)
app.register_blueprint(search_death.blueprint)
app.register_blueprint(search_drug.blueprint)
app.register_blueprint(search_person.blueprint)
app.register_blueprint(search_visit.blueprint)
app.register_blueprint(statistic_person.blueprint)
app.register_blueprint(statistic_visit.blueprint)

# === 스케줄러 등록 === #

refreshCondition()
refreshDrug()
refreshEthnicity()
refreshGender()
refreshRace()
refreshVisitType()

scheduler = BackgroundScheduler()
scheduler.add_job(refreshCondition, trigger='interval', hours=1)
scheduler.add_job(refreshDrug, trigger='interval', hours=1)
scheduler.add_job(refreshEthnicity, trigger='interval', hours=1)
scheduler.add_job(refreshGender, trigger='interval', hours=1)
scheduler.add_job(refreshRace, trigger='interval', hours=1)
scheduler.add_job(refreshVisitType, trigger='interval', hours=1)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

# === Flask 핸들러 정의 === #

@app.after_request
def afterRequest(response: Any) -> Any:
    '''
    Flask 요청이 처리된 이후 실행되는 핸들러입니다.

    Args:
        response (Any): 응답 메시지

    Returns:
        response (Any): 응답 메시지
    '''

    # --- 요청에 대한 로그 생성 --- #

    timestamp = datetime.datetime.today()

    time = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    log  = f'[{time}] {request.remote_addr} - {request.method} {request.path} - {response.status}'

    app.logger.info(log)

    return response

# === 메인 정의 === #

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)