#!/usr/bin/python3
import algobroker
algobroker.send("data",
                [
    {"dest": "broker_web",
     "cmd" : "set",     
     "assets" : ["3888.HK", "0700.HK", "0388.HK"]
     }
    ])

