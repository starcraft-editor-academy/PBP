# Preview Balance Patch for Starcraft: Remastered

[한국어](README.ko.md)

**PBP** is an user-created Preview Balance Patch for StarCraft: Remastered.

## Balance Changes in PBP 1.02

* Hydralisk:
  * Decreased hit points to 75.
  * Base Armor of Hydralisk changed from 0 to 1.
* Scout:
  * Now have a Detector ability.
* Vulture:
  * Now Spider Mines research is a 2 Level upgrade, 100/100 cost, 50 (fastest) seconds research.
  * Level 1: Every Vulture gains the ability to deploy Spider Mines, which provide each Vulture *two* Spider Mines to plant.
  * Level 2: Provide each Vulture *three* Spider Mines to plant. Every Vulture gains one additional Spider Mines.
* Fixed bug that prevent units from following any order until issue Stop, when move and attack orders are given in a short time.

## How to Build

* Put maps you want to apply patch to `basemap` folder.
* Run `generate_eds.py` with Python3.
* Run `make.ps1`. PBP patched maps will be generated in `output` folder.

## Links

* StarCraft EDitor ACademy (EDAC): https://cafe.naver.com/edac
