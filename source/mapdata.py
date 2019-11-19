#!/usr/bin/python
# -*- coding: utf-8 -*-

from eudplib import *

import upgrade

human = list()


def _init():
    for i in range(8):
        pinfo = GetPlayerInfo(i)
        if pinfo.typestr == "Human":
            global human
            human.append(i)


_init()

chkt = GetChkTokenized()
UPGx = bytearray(chkt.getsection("UPGx"))
TECx = bytearray(chkt.getsection("TECx"))
PUPx = bytearray(chkt.getsection("PUPx"))
PTEx = bytearray(chkt.getsection("PTEx"))
UNIx = bytearray(chkt.getsection("UNIx"))
MRGN = bytearray(chkt.getsection("MRGN"))


def SetLocation1(x, y):
    global MRGN
    MRGN[0:4] = i2b4(x)
    MRGN[4:8] = i2b4(y)
    MRGN[8:12] = i2b4(x)
    MRGN[12:16] = i2b4(y)


def applyMapData():
    SetLocation1(0, 1696)
    chkt.setsection("UPGx", UPGx)
    chkt.setsection("TECx", TECx)
    chkt.setsection("PUPx", PUPx)
    chkt.setsection("PTEx", PTEx)
    chkt.setsection("UNIx", UNIx)
    chkt.setsection("MRGN", MRGN)


def SetResearchSettings(research, data, value):
    global UPGx, TECx
    UPGx_data = {
        # data: (size, offset)
        "use default settings": (1, 0),
        # Unused 1 byte
        "base mineral cost": (2, 1 * 61 + 1),
        "mineral cost factor": (2, 3 * 61 + 1),
        "base gas cost": (2, 5 * 61 + 1),
        "gas cost factor": (2, 7 * 61 + 1),
        "base time": (2, 9 * 61 + 1),
        "time factor": (2, 11 * 61 + 1),
    }
    TECx_data = {
        # data: (size, offset)
        "use default settings": (1, 0),
        "mineral cost": (2, 1 * 44),
        "gas cost": (2, 3 * 44),
        "time": (2, 5 * 44),
        "energy cost": (2, 7 * 44),
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
    section[index : index + size] = i2bn(size)(value)


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
    section[index : index + size] = i2bn(size)(value)


def SetUnitSettings(
    *, unit, hit_points, shield_points, armor_points, build_time, mineral_cost, gas_cost
):
    global UNIx
    print(f" - {unit}")
    unit = EncodeUnit(unit)
    UNIx[unit] = 0
    hit_points *= 256
    shield_points *= 256
    UNIx_data = {
        # data: (size, offset)
        # "use_default_settings": (1, 0),
        "hit_points": (4, 1 * 228, hit_points),
        "shield_points": (2, 5 * 228, shield_points),
        "armor_points": (1, 7 * 228, armor_points),
        "build_time": (2, 8 * 228, build_time),
        "mineral_cost": (2, 10 * 228, mineral_cost),
        "gas_cost": (2, 12 * 228, gas_cost),
        # "string_number": (2, 14 * 228),
    }
    for name, data in UNIx_data.items():
        size, offset, value = data
        index = offset + unit * size
        orig_data = b2in(size)(UNIx[index : index + size])
        UNIx[index : index + size] = i2bn(size)(value)
        diff = "" if orig_data == value else "*"
        if name in ("hit_points", "shield_points"):
            orig_data, value = orig_data // 256, value // 256
        print(f"{diff}{name}: {orig_data} -> {value}")


def b2in(size):
    _b2in = {1: b2i1, 2: b2i2, 4: b2i4}
    return _b2in[size]


def i2bn(size):
    _i2bn = {1: i2b1, 2: i2b2, 4: i2b4}
    return _i2bn[size]
