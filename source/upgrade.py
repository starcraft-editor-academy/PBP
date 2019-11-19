#!/usr/bin/python
# -*- coding: utf-8 -*-

from eudplib import *

import mapdata

spider_mines = EUDArray(8)


def EnableSpiderMines(player):
    return CreateUnit(1, "Cave (Unused)", 1, player)


def detect_research():
    for p in mapdata.human:
        Trigger(
            conditions=[
                Research(p, "Spider Mines", Exactly, 1),
                Memory(spider_mines + 4 * p, Exactly, 0),
            ],
            actions=[
                EnableSpiderMines(p),
                SetResearch(p, "Spider Mines", Subtract, 1),
                SetMemory(spider_mines + 4 * p, Add, 1),
            ],
            preserved=False,
        )

        spider_mines_Lv2 = Forward()
        loopstart = Forward()
        loopend = Forward()

        spider_mines_Lv2 << RawTrigger(
            nextptr=loopend,
            conditions=[
                Research(p, "Spider Mines", Exactly, 1),
                Memory(spider_mines + 4 * p, Exactly, 1),
            ],
            actions=[
                SetMemory(spider_mines + 4 * p, Add, 1),
                SetNextPtr(spider_mines_Lv2, loopstart),
            ],
            preserved=False,
        )

        PushTriggerScope()
        loopstart << NextTrigger()
        for ptr, epd in EUDLoopPlayerUnit(p):
            unit_type = epd + 0x64 // 4
            if EUDIf()(MemoryEPD(unit_type, Exactly, EncodeUnit("Terran Vulture"))):
                spider_mine_count = epd + 0xC0 // 4
                Trigger(
                    conditions=MemoryEPD(spider_mine_count, AtMost, 2),
                    actions=SetMemoryEPD(spider_mine_count, Add, 1),
                )
            EUDEndIf()
        RawTrigger(
            nextptr=loopend, actions=SetNextPtr(spider_mines_Lv2, loopend),
        )
        PopTriggerScope()

        loopend << NextTrigger()


def Research(player, upgrade, cmptype, value):
    upgrade_id, category = EncodeUpgrade(upgrade)
    offset = category.Researched + player * category.length + upgrade_id
    multiplier = 256 ** (offset % 4)
    return MemoryX(offset, cmptype, value * multiplier, 255 * multiplier)


def SetResearch(player, upgrade, modifier, value):
    upgrade_id, category = EncodeUpgrade(upgrade)
    offset = category.Researched + player * category.length + upgrade_id
    multiplier = 256 ** (offset % 4)
    return SetMemoryX(offset, modifier, value * multiplier, 255 * multiplier)


class BaseUpgrade:
    pass


SCTech = None
SCUpgr = None
BWTech = None
BWUpgr = None

tech_dict = {
    "Stim Packs": 0,
    "Lockdown": 1,
    "EMP Shockwave": 2,
    "Spider Mines": 3,
    "Scanner Sweep": 4,
    "Siege Mode": 5,
    "Defensive Matrix": 6,
    "Irradiate": 7,
    "Yamato Gun": 8,
    "Cloaking Field": 9,
    "Personnel Cloaking": 10,
    "Burrowing": 11,
    "Infestation": 12,
    "Spawn Broodling": 13,
    "Dark Swarm": 14,
    "Plague": 15,
    "Consume": 16,
    "Ensnare": 17,
    "Parasite": 18,
    "Psionic Storm": 19,
    "Hallucination": 20,
    "Recall": 21,
    "Stasis Field": 22,
    "Archon Warp": 23,
    "Restoration": 24,
    "Disruption Web": 25,
    "Unknown Tech26": 26,
    "Mind Control": 27,
    "Dark Archon Meld": 28,
    "Feedback": 29,
    "Optical Flare": 30,
    "Maelstorm": 31,
    "Lurker Aspect": 32,
    "Unknown Tech33": 33,
    "Healing": 34,
    "Unknown Tech35": 35,
    "Unknown Tech36": 36,
    "Unknown Tech37": 37,
    "Unknown Tech38": 38,
    "Unknown Tech39": 39,
    "Unknown Tech40": 40,
    "Unknown Tech41": 41,
    "Unknown Tech42": 42,
    "Unknown Tech43": 43,
}
upgrade_dict = {
    "Terran Infantry Armor": 0,
    "Terran Vehicle Plating": 1,
    "Terran Ship Plating": 2,
    "Zerg Carapace": 3,
    "Zerg Flyer Caparace": 4,
    "Protoss Armor": 5,
    "Protoss Plating": 6,
    "Terran Infantry Weapons": 7,
    "Terran Vehicle Weapons": 8,
    "Terran Ship Weapons": 9,
    "Zerg Melee Attacks": 10,
    "Zerg Missile Attacks": 11,
    "Zerg Flyer Attacks": 12,
    "Protoss Ground Weapons": 13,
    "Protoss Air Weapons": 14,
    "Protoss Plasma Shields": 15,
    "U-238 Shells": 16,
    "Ion Thrusters": 17,
    "Burst Lasers (Unused)": 18,
    "Titan Reactor (SV +50)": 19,
    "Ocular Implants": 20,
    "Moebius Reactor (Ghost +50)": 21,
    "Apollo Reactor (Wraith +50)": 22,
    "Colossus Reactor (BC +50)": 23,
    "Ventral Sacs": 24,
    "Antennae": 25,
    "Pneumatized Carapace": 26,
    "Metabolic Boost": 27,
    "Adrenal Glands": 28,
    "Muscular Augments": 29,
    "Grooved Spines": 30,
    "Gamete Meiosis (Queen +50)": 31,
    "Metasynaptic Node (Defiler +50)": 32,
    "Singularity Charge": 33,
    "Leg Enhancements": 34,
    "Scarab Damage": 35,
    "Reaver Capacity": 36,
    "Gravitic Drive": 37,
    "Sensor Array": 38,
    "Gravitic Boosters": 39,
    "Khaydarin Amulet (HT +50)": 40,
    "Apial Sensors": 41,
    "Gravitic Thrusters": 42,
    "Carrier Capacity": 43,
    "Khaydarin Core (Arbiter +50)": 44,
    "Unknown Upgrade45": 45,
    "Unknown Upgrade46": 46,
    "Argus Jewel (Corsair +50)": 47,
    "Unknown Upgrade48": 48,
    "Argus Talisman (DA +50)": 49,
    "Unknown Upgrade50": 50,
    "Caduceus Reactor (Medic +50)": 51,
    "Chitinous Plating": 52,
    "Anabolic Synthesis": 53,
    "Charon Booster": 54,
    "Unknown Upgrade55": 55,
    "Unknown Upgrade56": 56,
    "Unknown Upgrade57": 57,
    "Unknown Upgrade58": 58,
    "Unknown Upgrade59": 59,
    "Unknown Upgrade60": 60,
}


def EncodeUpgrade(u):
    global tech_dict, upgrade_dict
    global SCTech, SCUpgr, BWTech, BWUpgr

    if u in tech_dict:
        upgrade_id = tech_dict[u]
        category = SCTech
        if upgrade_id >= SCTech.length:
            upgrade_id -= SCTech.length
            category = BWTech

    elif u in upgrade_dict:
        upgrade_id = upgrade_dict[u]
        category = SCUpgr
        if upgrade_id >= SCUpgr.length:
            upgrade_id -= SCUpgr.length
            category = BWUpgr

    return upgrade_id, category


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
