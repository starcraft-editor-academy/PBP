#!/usr/bin/python
# -*- coding: utf-8 -*-

from eudplib import *

import initialization
import unitloop
import upgrade


def onPluginStart():
    # 초기화 트리거는 initialization.py에 모음
    initialization.main()


def beforeTriggerExec():
    upgrade.detect_research()


def afterTriggerExec():
    unitloop.main()
    DoActions([
        # eudTurbo
        SetMemory(0x6509A0, SetTo, 0),
    ])
