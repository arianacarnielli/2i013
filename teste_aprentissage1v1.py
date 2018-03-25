# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 18:43:02 2018

@author: arian
"""

from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import Player
from soccersimulator.settings import *
from soccersimulator import Strategy

from soccersimulator import SoccerTeam, Simulation, show_simu,KeyboardStrategy,DTreeStrategy,load_jsonz,dump_jsonz
from soccersimulator import apprend_arbre, build_apprentissage, genere_dot

from aprentissage import *

import module as m
import sklearn
import numpy as np
import pickle
     
import autres.ortiz.ia as ia
list_ia = [ia]
import autres.sebastien.footIA as ia
list_ia.append(ia)
import autres.austenprinciple.Foot as ia
list_ia.append(ia)
import autres.ahmedmelliti.module as ia
list_ia.append(ia)
import autres.caieddy.module as ia
list_ia.append(ia)
import autres.iamlisa.module as ia 
list_ia.append(ia)
import autres.baladeur.modulesocc as ia
list_ia.append(ia)
import autres.aatarek.RepoSoccer_master as ia
list_ia.append(ia)
import autres.chefifarouck.FarouckYann as ia
list_ia.append(ia)
list_ia.append(m)


dic_strategy = {m.strategy.ShootStrat().name: m.strategy.ShootStrat(), m.strategy.DefStrat().name: m.strategy.DefStrat(),
                m.strategy.GardienStrat().name: m.strategy.GardienStrat(), m.strategy.DribleStrat().name: m.strategy.DribleStrat(),
                m.strategy.PassStrat().name: m.strategy.PassStrat(), m.strategy.AtkStrat().name: m.strategy.AtkStrat()}


nb_players = input('Nombre de joueurs : ')
nb_players = int(nb_players)

ent = entrainer(nb_players)

fname0 = "entrainer1v1_snap_teste_0"
fname1 = "entrainer2v2_snap_teste_1"

ent.entrainer_contre_tous(fname0 + ".jz")
# ent.entrainer2v2_snap(fname0 + ".jz", fname1 + ".jz", 5)

states_tuple0 = load_jsonz(fname0 + ".jz")
#states_tuple1 = load_jsonz(fname1 + ".jz")

ent.apprendre(states_tuple0,ent.my_get_features, fname0 + ".pkl")
#ent.apprendre(states_tuple1,ent.my_get_features, fname1 + ".pkl")

with open(fname0 + ".pkl","rb") as f:
    dt0 = pickle.load(f)
# Visualisation de l'arbre
genere_dot(dt0,fname0 + "arbre_entrainer2v2_snap_teste_0.dot")

#with open(fname1 + ".pkl","rb") as f:
#    dt1 = pickle.load(f)
# Visualisation de l'arbre
#genere_dot(dt1,fname1 + "arbre_entrainer2v2_snap_teste_1.dot")

treeStrat0 = DTreeStrategy(dt0, dic_strategy, ent.my_get_features)
#treeStrat1 = DTreeStrategy(dt1, dic_strategy, ent.my_get_features)

treeteam = SoccerTeam("Arbre Team")


test = input('Wanna test the ia? ')

if test == 'y':
    
    nb_ia = input('Against which team : ')
    nb_ia = int(nb_ia)
    
    team2 = list_ia[nb_ia].get_team(1)
    
    treeteam.add("Joueur 0",treeStrat0)
#    treeteam.add("Joueur 1",treeStrat1)

    simu = Simulation(treeteam,team2)
    show_simu(simu)

