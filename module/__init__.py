# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:29:15 2018

@author: 3525837
"""

from .toolbox import *
from .strategy import *

def get_team(d):
    myteam = SoccerTeam(name="MaTeam")
    for i in range(d):
        myteam.add("Joueur "+str(i) ,ShootBallStrategyOptimal())
    return myteam
