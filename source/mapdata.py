#!/usr/bin/python
# -*- coding: utf-8 -*-

from eudplib import *

human = list()


def init():
    for i in range(8):
        pinfo = GetPlayerInfo(i)
        if pinfo.typestr == "Human":
            global human
            human.append(i)


init()
