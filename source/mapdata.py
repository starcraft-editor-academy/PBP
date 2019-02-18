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


def applyMapData():
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
