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


spider_mines  = EUDArray(8)


def detect_research():
    global SCTech, SCUpgr, BWTech, BWUpgr
    for i in mapdata.human:
        RawTrigger(
            # [35] Unknown Tech35
            conditions=[
                Research(i, BWTech, 35, Exactly, 1),
                Memory(spider_mines + 4 * i, Exactly, 0),
            ],
            actions=[
                SetResearch(i, BWTech, 35, Subtract, 1),
                # [3] Spider Mines
                SetResearch(i, SCTech, 3, Add, 1),
                SetMemory(spider_mines + 4 * i, Add, 1),
            ],
            preserved=False,
        )

        spider_mines_Lv2 = Forward()
        loopstart = Forward()
        loopend = Forward()

        spider_mines_Lv2 << RawTrigger(
            nextptr=loopend,
            conditions=[
                Research(i, BWTech, 35, Exactly, 1),
                Memory(spider_mines + 4 * i, Exactly, 1),
            ],
            actions=[
                SetMemory(spider_mines + 4 * i, Add, 1),
                SetNextPtr(spider_mines_Lv2, loopstart),
            ],
            preserved=False,
        )

        PushTriggerScope()
        loopstart << NextTrigger()
        for ptr, epd in EUDLoopPlayerUnit(i):
            unit_type = epd + 0x64 // 4
            if EUDIf()([
                MemoryEPD(unit_type, Exactly,
                          EncodeUnit("Terran Vulture")),
            ]):
                spider_mine_count = epd + 0xC0 // 4
                if EUDIf()([
                    MemoryEPD(spider_mine_count, AtMost, 2),
                ]):
                    DoActions([
                        SetMemoryEPD(spider_mine_count, Add, 1),
                    ])
                EUDEndIf()
            EUDEndIf()
        RawTrigger(
            nextptr=loopend,
            actions=SetNextPtr(spider_mines_Lv2, loopend),
        )
        PopTriggerScope()

        loopend << NextTrigger()


def Research(player, category, upgrade_id, cmptype, value):
    upgrade_id = _process_upgrade_id(category, upgrade_id)
    offset = category.Researched + player * category.length + upgrade_id
    multiplier = 256 ** (offset % 4)
    return MemoryX(offset, cmptype, value * multiplier, 255 * multiplier)


def SetResearch(player, category, upgrade_id, modifier, value):
    upgrade_id = _process_upgrade_id(category, upgrade_id)
    offset = category.Researched + player * category.length + upgrade_id
    multiplier = 256 ** (offset % 4)
    return SetMemoryX(offset, modifier, value * multiplier, 255 * multiplier)


def _process_upgrade_id(category, upgrade_id):
    global SCTech, SCUpgr, BWTech, BWUpgr
    if category == BWTech:
        upgrade_id -= SCTech.length
    elif category == BWUpgr:
        upgrade_id -= SCUpgr.length
    return upgrade_id


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
