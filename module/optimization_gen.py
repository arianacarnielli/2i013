# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 15:53:44 2018

@author: arian
"""


from __future__ import print_function, division
from soccersimulator import SoccerTeam, Simulation, Strategy, show_simu, Vector2D
from soccersimulator.settings import *


from .action import *
from .toolbox import *
from .strategy import *
from .comportement import *
from .repeatsimu_gen import *

import random as rd
import math
import numpy as np

class ParamGenetique(object):
    def __init__(self, nb_players, trials = 5, max_steps = 2000, nb_individus = 20, pourcent_meilleurs = 0.25, pourcent_autres = 0.10, proba_mut = 0.05):
        self.nb_players = nb_players
        self.trials = trials
        self.max_steps = max_steps
        self.nb_individus = nb_individus
        self.proba_mut = proba_mut
        
        self.nb_meilleurs = max(int(nb_individus * pourcent_meilleurs), 1)
        self.nb_autres = max(int(nb_individus * pourcent_autres), 1)
        
        self.tab_params = np.empty(self.nb_individus, dtype = object)
        self.tab_points = np.empty(self.nb_individus)
        
        import autres.ortiz.ia as ia
        self.list_ia = [ia]
        import autres.sebastien.footIA as ia
        self.list_ia.append(ia)
        import autres.austenprinciple.Foot as ia
        self.list_ia.append(ia)
        import autres.ahmedmelliti.module as ia
        self.list_ia.append(ia)
        import autres.caieddy.module as ia
        self.list_ia.append(ia)
        import autres.iamlisa.module as ia 
        self.list_ia.append(ia)
        import autres.baladeur as ia
        self.list_ia.append(ia)
        import autres.aatarek.RepoSoccer_master.prog as ia
        self.list_ia.append(ia)
        import autres.chefifarouck.FarouckYann as ia
        self.list_ia.append(ia)

    def genVectAlea(self):
        accShoot = rd.randrange(0, 11, 1) / 10.
        accDrible = rd.randrange(0, 11, 1) / 10.
        vit = rd.randrange(0, 11, 1) / 10.
        nDrible = rd.randrange(0, 21, 1)
        maxAngle = round(rd.uniform(0, math.pi/2), 2)
        tooFar = rd.randrange(0, 61, 1)
        rSurfBut = rd.randrange(0, 51, 5)
        AngleHyst = round(rd.uniform(0, math.pi/10), 2)
        distShoot = rd.randrange(0, 76, 1)

        accShoot3 = rd.randrange(0, 11, 1) / 10.
#        accDrible2 = rd.randrange(0, 11, 1) / 10.
#        vit2 = rd.randrange(0, 11, 1) / 10.
#        nDrible2 = rd.randrange(0, 21, 1)
#        maxAngle2 = round(rd.uniform(0, math.pi/2), 2)
#        tooFar2 = rd.randrange(0, 61, 1)
#        rSurfBut2 = rd.randrange(0, 51, 5)
#        AngleHyst2 = round(rd.uniform(0, math.pi/10), 2)
        distShoot3 = rd.randrange(0, 76, 1)
        distMin3 = rd.randrange(0, 26, 1)
        distMax3 = rd.randrange(distMin3, 176, 1)
        rayon3 = rd.randrange(1, 26, 1)
        alpha3 = rd.randrange(0, 11, 1) / 10.
        
        p = rd.randrange(0, 16, 1) / 10.
        nDef = rd.randrange(0, 21, 1)
        alpha = rd.randrange(0, 11, 1) / 10.
        distMin = rd.randrange(0, 26, 1)
        distMax = rd.randrange(distMin, 176, 1)
        maxAngleDef = round(rd.uniform(0, math.pi/2), 2)
        rayon = rd.randrange(1, 26, 1)
        
        p2 = rd.randrange(0, 16, 1) / 10.
        nDef2 = rd.randrange(0, 21, 1)
        alpha2 = rd.randrange(0, 11, 1) / 10.
        distMin2 = rd.randrange(0, 26, 1)
        distMax2 = rd.randrange(distMin2, 176, 1)
        maxAngleDef2 = round(rd.uniform(0, math.pi/2), 2)
        rayon2 = rd.randrange(1, 26, 1)
        
        if self.nb_players==1:
            return [accShoot, accDrible, vit, nDrible, maxAngle, tooFar, \
                    rSurfBut, AngleHyst, alpha]
        elif self.nb_players==2:
            return [accShoot, accDrible, vit, nDrible, maxAngle, tooFar, \
                    rSurfBut, AngleHyst, distShoot, p, nDef, alpha, distMin, \
                    distMax, maxAngleDef, rayon]
        elif self.nb_players==4:
            return [accShoot, accDrible, vit, nDrible, maxAngle, tooFar, \
                    rSurfBut, AngleHyst, distShoot, p, nDef, alpha, distMin, \
                    distMax, maxAngleDef, rayon, \
                    distShoot3, accShoot3, distMin3, distMax3, rayon3, alpha3, \
                    p2, nDef2, alpha2, distMin2, distMax2, maxAngleDef2, rayon2]
    
    def test_against_all_ias(self, params, verbose = True):
        points = np.empty(len(self.list_ia))
        for i in range(len(self.list_ia)):
            if verbose:
                print("Test contre l'ia:",i)
            if self.nb_players==1:
                test = repeatsimu_gen1V1(params, self.list_ia[i], trials = self.trials, max_steps = self.max_steps)
            elif self.nb_players==2:
                test = repeatsimu_gen2V2(params, self.list_ia[i], trials = self.trials, max_steps = self.max_steps)
            elif self.nb_players==4:                
                test = repeatsimu_gen4V4(params, self.list_ia[i], trials = self.trials, max_steps = self.max_steps)
            test.start()
            points[i] = test.get_points()
            if verbose:
                print("Points contre l'ia {} : {}".format(i, points[i]))
        return points.sum()
    
    def init_params_alea(self):
        for i in range(self.nb_individus):
            self.tab_params[i] = self.genVectAlea()
            
    def init_params_results_from_file(self, filename):
        data = np.load(filename)
        self.tab_params = data["arr_0"]
        self.tab_points = data["arr_1"]

    def init_params_from_list(self, list_list_params):
        if len(list_list_params) > self.nb_meilleurs:
            raise Exception("Trop de joueurs dans la liste en argument!")
        for i in range(len(list_list_params)):
            self.tab_params[i] = list_list_params[i].copy()
        for i in range(len(list_list_params), self.nb_individus):
            self.tab_params[i] = self.genVectAlea()
            
    def eval_params(self):
        for i in range(self.nb_individus):
            self.tab_points[i] = self.test_against_all_ias(self.tab_params[i])
            
    def reproduction(self, parentA, parentB):
        fils = self.genVectAlea()
        for i in range(len(fils)):
            if rd.random() > self.proba_mut:
                if rd.random() < 0.5:
                    fils[i] = parentA[i]
                else:
                    fils[i] = parentB[i]
        return fils
            
    def next_generation(self):
        # Tableau avec les individus de la nouvelle generation.
        new_tab_params = np.empty_like(self.tab_params)
        
        # On trie les individus de l'ancienne generation par leurs points.
        index_sort = np.argsort(self.tab_points)
        index_sort = index_sort[::-1] # Changer l'ordre en decroissant.
        
        # On garde les nb_meilleurs dans la nouvelle generation.
        for i in range(self.nb_meilleurs):
            new_tab_params[i] = self.tab_params[index_sort[i]]
            
        # On choisi nb_autres aleatoires parmi les non-meilleurs pour les
        # garder aussi et avoir donc encore de la diversite.
        index_autres = np.random.choice(index_sort[self.nb_meilleurs:], size = self.nb_autres, replace = False)
            
        for i in range(self.nb_autres):
            new_tab_params[self.nb_meilleurs + i] = self.tab_params[index_autres[i]]
            
        # Pour chaque nouvel individu qu'il reste a creer:
        for i in range(self.nb_meilleurs + self.nb_autres, self.nb_individus):
            # Choix de deux parents
            parents = np.random.choice(new_tab_params[:(self.nb_meilleurs + self.nb_autres)], size = 2, replace = False)
            # Création du fils
            new_tab_params[i] = self.reproduction(parents[0], parents[1])
            
        self.tab_params = new_tab_params
        
    def start_alea(self, nb_generations = 10):
        self.init_params_alea()
        for i in range(nb_generations):
            self.eval_params()
            np.savez("genetique_{}_{}_20180407".format(self.nb_players, i), self.tab_params, self.tab_points)
            self.next_generation()
        self.eval_params()
        np.savez("genetique_{}_final_20180407".format(self.nb_players), self.tab_params, self.tab_points)
        
    def start_file(self, filename, nb_generations = 10):
        self.init_params_results_from_file(filename)
        
        for i in range(nb_generations):
            self.next_generation()
            self.eval_params()
            np.savez("genetique_{}_{}_20180407".format(self.nb_players, i), self.tab_params, self.tab_points)
            
    def start_list(self, list_list_params, nb_generations = 10):
        self.init_params_from_list(list_list_params)
        for i in range(nb_generations):
            self.eval_params()
            np.savez("genetique_{}_{}_20180407".format(self.nb_players, i), self.tab_params, self.tab_points)
            self.next_generation()
        self.eval_params()
        np.savez("genetique_{}_final_20180407".format(self.nb_players), self.tab_params, self.tab_points)