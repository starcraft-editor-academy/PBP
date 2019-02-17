#!/usr/bin/python
# -*- coding: utf-8 -*-

from eudplib import *

import mapdata
import upgrade

chkt = GetChkTokenized()
UPGx = bytearray(chkt.getsection("UPGx"))
TECx = bytearray(chkt.getsection("TECx"))
PUPx = bytearray(chkt.getsection("PUPx"))
PTEx = bytearray(chkt.getsection("PTEx"))
UNIx = bytearray(chkt.getsection("UNIx"))


def main():
    DoActions([
        # 스카웃 디텍터 추가
        SetMemory(
            0x664080 + EncodeUnit("Protoss Scout") * 4,
            Add, 32768),
        # 머신샵 Spider Mines 버튼에서 [18] Burst Lasers 업그레이드 사용
        SetMemory(0x5186E8, SetTo, 4363344),
        SetMemory(0x5186EC, SetTo, 4338448),
        SetMemory(0x5186F0, SetTo, 1179666),
        # Burst Lasers 업그레이드 아이콘, 이름 변경
        SetMemory(0x655A40 + 18 * 2, Subtract, 113),
        SetMemory(0x655AC0 + 18 * 2, Add, 4),
    ])

    # Burst Lasers 업그레이드 비용 100/100, 시간 1200
    SetResearchSettings("Burst Lasers (Unused)", "base mineral cost", 100)
    SetResearchSettings("Burst Lasers (Unused)", "mineral cost factor", 0)
    SetResearchSettings("Burst Lasers (Unused)", "base gas cost", 100)
    SetResearchSettings("Burst Lasers (Unused)", "gas cost factor", 0)
    SetResearchSettings("Burst Lasers (Unused)", "base time", 1200)
    SetResearchSettings("Burst Lasers (Unused)", "time factor", 0)

    # Burst Lasers 업그레이드 최대 2 단계
    SetResearchRestrictions("Burst Lasers (Unused)", "global maximum level", 2)
    SetResearchRestrictions("Burst Lasers (Unused)", "global starting level", 0)
    for p in mapdata.human:
        SetResearchRestrictions("Burst Lasers (Unused)", "use global defaults", True, player=p)

    # 히드라리스크 체력을 75로 하향, 방어력을 1로 상향.
    SetUnitSettings("Zerg Hydralisk", "hit points", 75)
    SetUnitSettings("Zerg Hydralisk", "armor points", 1)

    global chkt, UPGx, TECx, PUPx, PTEx, UNIx
    chkt.setsection("UPGx", UPGx)
    chkt.setsection("TECx", TECx)
    chkt.setsection("PUPx", PUPx)
    chkt.setsection("PTEx", PTEx)
    chkt.setsection("UNIx", UNIx)


def SetResearchSettings(research, data, value):
    global UPGx, TECx
    UPGx_data = {
        # data: (size, offset)
        "use default settings": (1, 0),
        # Unused 1 byte
        "base mineral cost":    (2, 1 * 61 + 1),
        "mineral cost factor":  (2, 3 * 61 + 1),
        "base gas cost":        (2, 5 * 61 + 1),
        "gas cost factor":      (2, 7 * 61 + 1),
        "base time":            (2, 9 * 61 + 1),
        "time factor":          (2, 11 * 61 + 1),
    }
    TECx_data = {
        # data: (size, offset)
        "use default settings": (1, 0),
        "mineral cost":         (2, 1 * 44),
        "gas cost":             (2, 3 * 44),
        "time":                 (2, 5 * 44),
        "energy cost":          (2, 7 * 44),
    }
    try:
        research_id = upgrade.tech_dict[research]
    except (KeyError):
        try:
            research_id = upgrade.upgrade_dict[research]
        except (KeyError):
            raise EPError("%s is not an Upgrade/Tech." % research)
        else:
            section = UPGx
            research_data = UPGx_data
            research_keys = UPGx_data.keys()
    else:
        section = TECx
        research_data = TECx_data
        research_keys = TECx_data.keys()
    assert data in research_data, "%s is not an Upgrade/Tech Settings." % (data)
    section[research_id] = 0
    size, offset = research_data[data]
    index = offset + research_id * size
    section[index:index + size] = i2bn(size)(value)


def SetResearchRestrictions(research, data, value, player=False):
    global PUPx, PTEx
    PUPx_data = {
        "length": 61,
        # data: (size, offset, player)
        "player maximum level": (1, 0, True),
        "player starting level": (1, 1 * 12 * 61, True),
        "global maximum level": (1, 2 * 12 * 61, False),
        "global starting level": (1, (1 + 2 * 12) * 61, False),
        "use global defaults": (1, (2 + 2 * 12) * 61, True),
    }
    PTEx_data = {
        "length": 44,
        # data: (size, offset, player)
        "player availability": (1, 0, True),
        "already researched": (1, 1 * 12 * 44, True),
        "global availability": (1, 2 * 12 * 44, False),
        "global already researched": (1, (1 + 2 * 12) * 44, False),
        "use global defaults": (1, (2 + 2 * 12) * 44, True),
    }
    try:
        research_id = upgrade.tech_dict[research]
    except (KeyError):
        try:
            research_id = upgrade.upgrade_dict[research]
        except (KeyError):
            raise EPError("%s is not an Upgrade/Tech." % research)
        else:
            section = PUPx
            research_data = PUPx_data
            research_keys = PUPx_data.keys()
    else:
        section = PTEx
        research_data = PTEx_data
        research_keys = PTEx_data.keys()
    assert data in research_data, "%s is not an Upgrade/Tech Restrictions." % (data)
    size, offset, use_player = research_data[data]
    index = offset + research_id * size
    if player and use_player:
        index += research_data["length"] * player
    section[index:index + size] = i2bn(size)(value)


def SetUnitSettings(unit, data, value):
    global UNIx
    UNIx_data = {
        # data: (size, offset)
        "use default settings": (1, 0),
        "hit points":           (4, 1 * 228),
        "shield points":        (2, 5 * 228),
        "armor points":         (1, 7 * 228),
        "build time":           (2, 8 * 228),
        "mineral cost":         (2, 10 * 228),
        "gas cost":             (2, 12 * 228),
        "string number":        (2, 14 * 228),
    }
    UNIx_keys = UNIx_data.keys()
    if data in ("hit points", "shield points"):
        value = value * 256
    unit = EncodeUnit(unit)
    assert data in UNIx_data, "%s is not an Unit Settings." % (data)
    UNIx[unit] = 0
    size, offset = UNIx_data[data]
    index = offset + unit * size
    UNIx[index:index + size] = i2bn(size)(value)


def i2bn(size):
    _i2bn = {
        1: i2b1,
        2: i2b2,
        4: i2b4,
    }
    return _i2bn[size]
