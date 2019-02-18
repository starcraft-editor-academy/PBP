#!/usr/bin/python
# -*- coding: utf-8 -*-

from eudplib import *

from mapdata import (SetResearchRestrictions, SetResearchSettings,
                     SetUnitSettings, applyMapData)


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
    for p in range(12):
        SetResearchRestrictions("Burst Lasers (Unused)", "use global defaults", True, player=p)

    # 히드라리스크 체력을 75로 하향, 방어력을 1로 상향.
    SetUnitSettings("Zerg Hydralisk", "hit points", 75)
    SetUnitSettings("Zerg Hydralisk", "armor points", 1)

    applyMapData()
