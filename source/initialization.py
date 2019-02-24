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
        # Spider Mines 기술사용 요구사항 수정
		SetMemory(0x514A90, SetTo, 0xFF240003),
		SetMemory(0x514A94, SetTo, 0x00B3FF03),
        SetMemory(0x66167C, SetTo, 131074),
		SetMemory(0x662B2C, SetTo, 0),
		SetMemory(0x6632E8, SetTo, 592137),
		SetMemory(0x66434C, SetTo, 603979781),
    ])

    # 히드라리스크 체력을 75로 하향, 방어력을 1로 상향.
    SetUnitSettings("Zerg Hydralisk", "hit points", 75)
    SetUnitSettings("Zerg Hydralisk", "armor points", 1)

    applyMapData()
