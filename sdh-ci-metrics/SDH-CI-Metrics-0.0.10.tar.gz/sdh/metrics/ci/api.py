"""
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
  This file is part of the Smart Developer Hub Project:
    http://www.smartdeveloperhub.org

  Center for Open Middleware
        http://www.centeropenmiddleware.com/
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
  Copyright (C) 2015 Center for Open Middleware.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

            http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
"""

__author__ = 'Fernando Serena'

from sdh.metrics.ci import app, st as store
from sdh.metrics.store.metrics import aggregate, avg
import calendar
from datetime import datetime
import math


@app.orgmetric('/total-builds', 'sum', 'builds', title='Builds')
def get_total_builds(**kwargs):
    return [len(store.get_builds())]


@app.repometric('/total-repo-builds', 'sum', 'builds', title='Builds')
def get_repo_builds(rid, **kwargs):
    return [len(store.get_repo_builds(rid))]


@app.orgmetric('/avg-builds', 'avg', 'builds', title='Builds')
def get_avg_builds(**kwargs):
    return avg([len(store.get_repo_builds(rid)) for rid in store.get_repositories()])


@app.orgmetric('/total-executions', 'sum', 'executions', title='Jobs')
def get_total_executions(**kwargs):
    return aggregate(store, 'metrics:total-jobs', kwargs['begin'], kwargs['end'], kwargs['max'])


@app.orgmetric('/total-passed-builds', 'sum', 'passedbuilds', title='Success builds')
def get_total_passed_builds(**kwargs):
    success_builds = 0
    for build in store.get_builds():
        last_passed = store.get_last_passed_execution(build, kwargs['begin'], kwargs['end'])
        if last_passed:
            success_builds += 1
    return {}, [success_builds]


@app.orgmetric('/total-failed-builds', 'sum', 'failedbuilds', title='Broken builds')
def get_total_failed_builds(**kwargs):
    failed_builds = 0
    for build in store.get_builds():
        last_passed = store.get_last_passed_execution(build, kwargs['begin'], kwargs['end'])
        if not last_passed or last_passed is None:
            failed_builds += 1
    return {}, [failed_builds]


@app.orgmetric('/total-passed-executions', 'sum', 'passedexecutions', title='Success jobs')
def get_total_passed_executions(**kwargs):
    return aggregate(store, 'metrics:total-passed-jobs', kwargs['begin'], kwargs['end'], kwargs['max'])


@app.orgmetric('/total-failed-executions', 'sum', 'failedexecutions', title='Broken jobs')
def get_total_failed_executions(**kwargs):
    return aggregate(store, 'metrics:total-failed-jobs', kwargs['begin'], kwargs['end'], kwargs['max'])


@app.repometric('/total-repo-executions', 'sum', 'executions', title='Jobs')
def get_total_repo_executions(rid, **kwargs):
    return aggregate(store, 'metrics:total-repo-jobs:{}'.format(rid), kwargs['begin'], kwargs['end'], kwargs['max'])


@app.repometric('/avg-repo-executions', 'avg', 'executions', title='Jobs')
def get_avg_repo_executions(rid, **kwargs):
    return aggregate(store, 'metrics:total-repo-jobs:{}'.format(rid), kwargs['begin'], kwargs['end'], kwargs['max'],
                     aggr=avg)


@app.repometric('/total-passed-repo-executions', 'sum', 'passedexecutions', title='Success jobs')
def get_total_passed_repo_executions(rid, **kwargs):
    return aggregate(store, 'metrics:total-passed-repo-jobs:{}'.format(rid), kwargs['begin'], kwargs['end'],
                     kwargs['max'])


@app.repometric('/total-failed-repo-executions', 'sum', 'failedexecutions', title='Broken jobs')
def get_total_failed_repo_executions(rid, **kwargs):
    return aggregate(store, 'metrics:total-failed-repo-jobs:{}'.format(rid), kwargs['begin'], kwargs['end'],
                     kwargs['max'])


@app.repotbd('/repo-build-time', 'buildtime', title='Build time')
def get_repo_build_time(rid, **kwargs):
    total = store.get_repo_build_time(rid, begin=kwargs['begin'], end=kwargs['end'])
    if math.isnan(total):
        return []
    return [total]


@app.orgtbd('/avg-build-time', 'avgbuildtime', title='Build time')
def get_avg_build_time(**kwargs):
    average = avg(
        [store.get_repo_build_time(rid, begin=kwargs['begin'], end=kwargs['end']) for rid in store.get_repositories()])
    if math.isnan(average):
        return []
    return [average]


@app.orgtbd('/total-build-time', 'buildtime', title='Build time')
def get_total_build_time(**kwargs):
    total = sum(
        [store.get_repo_build_time(rid, begin=kwargs['begin'], end=kwargs['end']) for rid in store.get_repositories()])
    if math.isnan(total):
        return []

    return [total]


@app.orgtbd('/total-broken-time', 'brokentime', title='Broken time')
def get_total_broken_time(**kwargs):
    return [sum([store.get_broken_time(rid) for rid in store.get_repositories()])]


@app.repometric('/repo-broken-time', 'sum', 'brokentime', title='Broken time')
def get_repo_broken_time(rid, **kwargs):
    begin = kwargs['begin']
    if begin is None:
        begin = 0
    end = kwargs['end']
    if end is None:
        end = calendar.timegm(datetime.now().timetuple())

    return {'begin': begin, 'end': end}, [store.get_broken_time(rid, begin=begin, end=end)]


@app.repotbd('/repo-time-to-fix', 'timetofix', title='Time to fix')
def get_repo_time_to_fix(rid, **kwargs):
    begin = kwargs['begin']
    if begin is None:
        begin = 0
    end = kwargs['end']
    if end is None:
        end = calendar.timegm(datetime.now().timetuple())

    return [store.get_time_to_fix(rid, begin=begin, end=end)]


@app.orgtbd('/time-to-fix', 'timetofix', title='Time to fix')
def get_time_to_fix(**kwargs):
    begin = kwargs['begin']
    if begin is None:
        begin = 0
    end = kwargs['end']
    if end is None:
        end = calendar.timegm(datetime.now().timetuple())

    return [avg([store.get_time_to_fix(rid, begin=begin, end=end) for rid in store.get_repositories()])]
