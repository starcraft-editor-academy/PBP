#!/usr/bin/python
# -*- coding: utf-8 -*-

from eudplib import *

import mapdata

SCTech = None
SCUpgr = None
BWTech = None
BWUpgr = None


class BaseUpgrade:
    pass


ion_thrusters = EUDArray(8)
spider_mines  = EUDArray(8)


def detect_research():
    global SCTech, SCUpgr, BWTech, BWUpgr
    for i in mapdata.human:
        RawTrigger(
            # [17] ion_thrusters
            conditions=IsResearched(i, SCUpgr, 17, Exactly, 1),
            actions=SetMemory(ion_thrusters + 4 * i, Add, 1),
            preserved=False,
        )
        RawTrigger(
            # [3] spider_mines
            conditions=IsResearched(i, SCTech, 3, Exactly, 1),
            actions=SetMemory(spider_mines + 4 * i, Add, 1),
            preserved=False,
        )


def IsResearched(player, category, upgrade_id, cmptype, value):
    offset = category.Researched + player * category.length + upgrade_id
    multiplier = 256 ** (offset % 4)
    return MemoryX(offset, cmptype, value * multiplier, 255 * multiplier)


def init():
    global SCTech, SCUpgr, BWTech, BWUpgr
    SCTech, SCUpgr, BWTech, BWUpgr = [BaseUpgrade() for _ in range(4)]

    SCTech.Available = 0x58CE24
    SCTech.Researched = 0x58CF44
    SCTech.length = 24

    SCUpgr.Available = 0x58D088
    SCUpgr.Researched = 0x58D2B0
    SCUpgr.length = 46

    BWTech.Available = 0x58F050
    BWTech.Researched = 0x58F140
    BWTech.length = 20

    BWUpgr.Available = 0x58F278
    BWUpgr.Researched = 0x58F32C
    BWUpgr.length = 15


init()
