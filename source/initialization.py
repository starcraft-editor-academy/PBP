#!/usr/bin/python
# -*- coding: utf-8 -*-

from eudplib import *

chkt = GetChkTokenized()
UNIx = bytearray(chkt.getsection("UNIx"))


def main():
    DoActions([
        # 스카웃 디텍터 추가
        SetMemory(0x664198, Add, 32768),
        # 머신샵 Spider Mines 테크 대신 [18] Burst Lasers 업그레이드 사용
        SetMemory(0x5186E8, SetTo, 4363344),
        SetMemory(0x5186EC, SetTo, 4338448),
        SetMemory(0x5186F0, SetTo, 1179666),
        # Burst Lasers 업그레이드 아이콘, 이름 변경
        SetMemory(0x655AE4, Add, 4),
        SetMemory(0x655A64, Subtract, 113),
        # Burst Lasers 업그레이드 비용, 시간 변경
        SetMemory(0x655764, Subtract, 100),
        SetMemory(0x655864, Subtract, 100),
        SetMemory(0x655BA4, Subtract, 1000),
        # Burst Lasers 업그레이드 요구사항 변경
        SetMemory(0x6558E4, SetTo, 15270115),
        # Burst Lasers 업그레이드 단계 변경
        SetMemory(0x58D088 + 0 * 46 + 18, Add, 2 * 65536),
        SetMemory(0x58D088 + 1 * 46 + 18, Add, 2),
        SetMemory(0x58D088 + 2 * 46 + 18, Add, 2 * 65536),
        SetMemory(0x58D088 + 3 * 46 + 18, Add, 2),
        SetMemory(0x58D088 + 4 * 46 + 18, Add, 2 * 65536),
        SetMemory(0x58D088 + 5 * 46 + 18, Add, 2),
        SetMemory(0x58D088 + 6 * 46 + 18, Add, 2 * 65536),
        SetMemory(0x58D088 + 7 * 46 + 18, Add, 2),
    ])
    # 히드라리스크 체력을 75로 하향, 방어력을 1로 상향.
    SetUnitSettings("Zerg Hydralisk", "hit points", 75)
    SetUnitSettings("Zerg Hydralisk", "armor points", 1)

    global chkt, UNIx
    chkt.setsection("UNIx", UNIx)


def SetUnitSettings(unit, data, value):
    global UNIx
    UNIx_data = {
        # data: (offset, size)
        "use default settings": (0, 1),
        "hit points":           (1, 4),
        "shield points":        (5, 2),
        "armor points":         (7, 1),
        "build time":           (8, 2),
        "mineral cost":         (10, 2),
        "gas cost":             (12, 2),
        "string number":        (14, 2),
    }
    UNIx_keys = UNIx_data.keys()
    if data in ("hit points", "shield points"):
        value = value * 256
    unit = EncodeUnit(unit)
    assert data in UNIx_data, "%s is not an Unit Settings." % (data)
    UNIx[unit] = 0
    offset, size = UNIx_data[data]
    index = 228 * offset + unit * size
    i2bn = {
        1: i2b1,
        2: i2b2,
        4: i2b4,
    }
    UNIx[index:index + size] = i2bn[size](value)
