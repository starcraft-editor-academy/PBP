#!/usr/bin/python
# -*- coding: utf-8 -*-

from eudplib import *

import initialization
import mapdata
import unitloop
import upgrade

with open("../source/VERSION", "r") as f:
    VERSION = f.read()


def onPluginStart():
    edit_map_title_and_description()
    # 초기화 트리거는 initialization.py에 모음
    initialization.main()


def beforeTriggerExec():
    upgrade.detect_research()


def afterTriggerExec():
    unitloop.main()
    f_dwwrite(0x6509A0, 0)  # eudTurbo


def edit_map_title_and_description():
    chkt = mapdata.chkt
    SPRP = chkt.getsection("SPRP")
    strmap = TBL(chkt.getsection("STR"))

    title_strid = b2i2(SPRP, 0)
    desc_strid = b2i2(SPRP, 2)
    title = strmap.GetString(title_strid)
    desc = strmap.GetString(desc_strid)

    try:
        title = GetStringIndex(title + u2b(" \x06PBP %s" % VERSION))
    except (TypeError):
        pass
    else:
        desc = GetStringIndex(
            desc + u2b("\nEdited by EDAC https://cafe.naver.com/edac")
        )
        SPRP = i2b2(title) + i2b2(desc)
        chkt.setsection("SPRP", SPRP)
