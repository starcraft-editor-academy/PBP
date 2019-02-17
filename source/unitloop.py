#!/usr/bin/python
# -*- coding: utf-8 -*-

from eudplib import *

import upgrade


def main():
    for ptr, epd in LoopNewUnit(31):
        unit_type = epd + 0x64 // 4
        if EUDIf()(
            MemoryEPD(unit_type, Exactly,
                      EncodeUnit("Terran Vulture"))
        ):
            spider_mine_count = epd + 0xC0 // 4
            EUDContinueIfNot(
                MemoryXEPD(spider_mine_count, Exactly, 3, 0xFF)
            )
            player = f_bread_epd(epd + 0x4C // 4, 0)
            Trigger(
                conditions=MemoryEPD(EPD(upgrade.spider_mines) + player, AtMost, 1),
                actions=SetMemoryEPD(spider_mine_count, Subtract, 1),
            )
        EUDEndIf()

    for ptr, epd in EUDLoopUnit2():
        # 비건물에 betterBrain 적용
        status_flags    = epd + 0xDC // 4
        current_speed1  = epd + 0x38 // 4
        current_speed2  = epd + 0x3C // 4
        current_speed   = epd + 0x40 // 4
        movement_flags  = epd + 0x20 // 4

        if EUDIf()(EUDSCAnd()
            (MemoryXEPD(status_flags, Exactly, 0, 2))
            (MemoryEPD(current_speed1, Exactly, 0))
            (MemoryEPD(current_speed2, Exactly, 0))
            (MemoryEPD(current_speed, Exactly, 0))
            (MemoryXEPD(movement_flags, Exactly, 0x12, 0xFF))
        ()):
            DoActions([
                SetMemoryEPD(movement_flags, Subtract, 0x12),
            ])
        EUDEndIf()


def LoopNewUnit(allowance=2):
    firstUnitPtr = EPD(0x628430)
    EUDCreateBlock('newunitloop', 'newlo')
    tos0 = EUDLightVariable()
    tos0 << 0

    ptr, epd = f_cunitepdread_epd(firstUnitPtr)
    if EUDWhile()(ptr >= 1):
        tos = epd + 0xA5 // 4
        if EUDIf()(MemoryXEPD(tos, AtLeast, 0x100, 0xFF00)):
            DoActions(SetMemoryXEPD(tos, SetTo, 0, 0xFF00))
            yield ptr, epd
        if EUDElse()():
            DoActions(tos0.AddNumber(1))
            EUDBreakIf(tos0.AtLeast(allowance))
        EUDEndIf()
        EUDSetContinuePoint()
        SetVariables([ptr, epd], f_cunitepdread_epd(epd + 1))
    EUDEndWhile()

    EUDPopBlock('newunitloop')
