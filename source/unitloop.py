#!/usr/bin/python
# -*- coding: utf-8 -*-

from eudplib import *

import upgrade


def main():
    for ptr, epd in LoopNewUnit(31):
        unit_type = epd + 0x64 // 4
        if EUDIf()(MemoryEPD(unit_type, Exactly, EncodeUnit("Terran Vulture"))):
            spider_mine_count = epd + 0xC0 // 4
            EUDContinueIfNot(MemoryXEPD(spider_mine_count, Exactly, 3, 0xFF))
            player = f_bread_epd(epd + 0x4C // 4, 0)
            Trigger(
                conditions=MemoryEPD(EPD(upgrade.spider_mines) + player, AtMost, 1),
                actions=SetMemoryEPD(spider_mine_count, Subtract, 1),
            )
        EUDEndIf()

    for ptr, epd in EUDLoopUnit2():
        # 비건물에 betterBrain 적용
        status_flags = epd + 0xDC // 4
        current_speed1 = epd + 0x38 // 4
        current_speed2 = epd + 0x3C // 4
        current_speed = epd + 0x40 // 4
        movement_flags = epd + 0x20 // 4

        if EUDIf()(
            EUDSCAnd()(MemoryXEPD(status_flags, Exactly, 0, 2))(
                MemoryEPD(current_speed1, Exactly, 0)
            )(MemoryEPD(current_speed2, Exactly, 0))(
                MemoryEPD(current_speed, Exactly, 0)
            )(
                MemoryXEPD(movement_flags, Exactly, 0x12, 0xFF)
            )()
        ):
            f_dwsubtract_epd(movement_flags, 0x12)
        EUDEndIf()


newCUnit = EUDArray(1700 * 336)
epd2newCUnit = EPD(newCUnit) - EPD(0x59CCA8)


def EUDLoopUnit2():
    """EUDLoopUnit보다 약간? 빠릅니다. 유닛 리스트를 따라가지 않고
    1700개 유닛을 도는 방식으로 작동합니다.
    """
    ptr, epd = EUDCreateVariables(2)
    DoActions(ptr.SetNumber(0x59CCA8), epd.SetNumber(EPD(0x59CCA8)))
    if EUDLoopN()(1700):
        # orderID가 0(Die)이면 없는 유닛으로 판단.
        if EUDIf()(MemoryXEPD(epd + (0x4D // 4), Exactly, 0, 0xFF00)):
            global epd2newCUnit
            f_dwwrite_epd(epd + epd2newCUnit, 0)
            EUDContinue()
        EUDEndIf()
        yield ptr, epd
        EUDSetContinuePoint()
        DoActions(ptr.AddNumber(336), epd.AddNumber(336 // 4))
    EUDEndLoopN()


def LoopNewUnit(allowance=2):
    firstUnitPtr = EPD(0x628430)
    EUDCreateBlock("newunitloop", "newlo")
    tos0 = EUDLightVariable()
    tos0 << 0

    ptr, epd = f_cunitepdread_epd(firstUnitPtr)
    if EUDWhile()(ptr >= 1):
        tos1 = f_bread_epd(epd + 0xA5 // 4, 1)
        global epd2newCUnit
        tos2 = epd + epd2newCUnit
        if EUDIfNot()(MemoryEPD(tos2, Exactly, tos1)):
            DoActions(SetMemoryEPD(tos2, SetTo, tos1))
            yield ptr, epd
        if EUDElse()():
            DoActions(tos0.AddNumber(1))
            EUDBreakIf(tos0.AtLeast(allowance))
        EUDEndIf()
        EUDSetContinuePoint()
        f_cunitepdread_epd(epd + 1, ret=[ptr, epd])
    EUDEndWhile()

    EUDPopBlock("newunitloop")
