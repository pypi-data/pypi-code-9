# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###

from .api.balancer_balancer_name_frontend import BalancerBalancerNameFrontend
from .api.balancer_balancer_name_backends import BalancerBalancerNameBackends
from .api.balancer_balancer_name_entrypoints import BalancerBalancerNameEntrypoints
from .api.nginx import Nginx
from .api.balancer_names_prefix import BalancerNamesPrefix
from .api.nginx_name import NginxName
from .api.nginx_name_upstream import NginxNameUpstream
from .api.balancer import Balancer
from .api.balancer_balancer_name import BalancerBalancerName
from .api.slaves import Slaves
from .api.nginx_name_server import NginxNameServer


routes = [
    dict(resource=BalancerBalancerNameFrontend, urls=['/balancer/<balancer_name>/frontend'], endpoint='balancer_balancer_name_frontend'),
    dict(resource=BalancerBalancerNameBackends, urls=['/balancer/<balancer_name>/backends'], endpoint='balancer_balancer_name_backends'),
    dict(resource=BalancerBalancerNameEntrypoints, urls=['/balancer/<balancer_name>/entrypoints'], endpoint='balancer_balancer_name_entrypoints'),
    dict(resource=Nginx, urls=['/nginx'], endpoint='nginx'),
    dict(resource=BalancerNamesPrefix, urls=['/balancer/names/<prefix>'], endpoint='balancer_names_prefix'),
    dict(resource=NginxName, urls=['/nginx/<name>'], endpoint='nginx_name'),
    dict(resource=NginxNameUpstream, urls=['/nginx/<name>/upstream'], endpoint='nginx_name_upstream'),
    dict(resource=Balancer, urls=['/balancer'], endpoint='balancer'),
    dict(resource=BalancerBalancerName, urls=['/balancer/<balancer_name>'], endpoint='balancer_balancer_name'),
    dict(resource=Slaves, urls=['/slaves'], endpoint='slaves'),
    dict(resource=NginxNameServer, urls=['/nginx/<name>/server'], endpoint='nginx_name_server'),
]