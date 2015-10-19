#!/usr/bin/env python
from etatimer import EtaTimer
import time

x = list(range(20))
t = EtaTimer(len(x))
for i in x:
    t.tick()
    time.sleep(1)
