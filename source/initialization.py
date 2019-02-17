#!/usr/bin/python
# -*- coding: utf-8 -*-

from eudplib import *

chkt = GetChkTokenized()
UNIx = bytearray(chkt.getsection("UNIx"))


def main():
    DoActions([
        # 스카웃 디텍터 추가
        SetMemory(0x664198, Add, 32768),
        # 머신 샵의 Spider Mines 버튼 액션을 Unknown Tech35로
        SetMemory(0x5186F0, Add, 2097152),
        # Unknown Tech35를 Spider Mines처럼 수정
		SetMemory(0x656234, SetTo, 6553600),
		SetMemory(0x65628C, SetTo, 6553600),
		SetMemory(0x6562E4, SetTo, 20710618),
		SetMemory(0x6563C4, SetTo, 1),
		SetMemory(0x65641C, SetTo, 78643200),
		SetMemory(0x656474, SetTo, 15925613),
		SetMemory(0x6564A8, SetTo, 16843520),
		SetMemory(0x6564D4, SetTo, 65793),
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
