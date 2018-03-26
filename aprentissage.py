# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 18:25:44 2018

@author: 3525837
"""

from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import Player
from soccersimulator.settings import *
from soccersimulator import Strategy
from soccersimulator import SimuGUI, pyg_start

from soccersimulator import SoccerTeam, Simulation, show_simu,KeyboardStrategy,DTreeStrategy,load_jsonz,dump_jsonz
from soccersimulator import apprend_arbre, build_apprentissage, genere_dot

import module as m
import sklearn
import numpy as np
import pickle
import random as rd

assert sklearn.__version__ >= "0.18.1","Updater sklearn !! (pip install -U sklearn --user )"

class entrainer(object):

    def __init__(self, nb_players):
        
        self.nb_players = nb_players     
        import autres.ortiz.ia as ia
        self.list_ia = [ia]
        import autres.sebastien.footIAT2 as ia
        self.list_ia.append(ia)
        import autres.austenprinciple.Foot as ia
        self.list_ia.append(ia)
        import autres.ahmedmelliti.module as ia
        self.list_ia.append(ia)
        import autres.caieddy.module as ia
        self.list_ia.append(ia)
        import autres.iamlisa.module as ia 
        self.list_ia.append(ia)
        import autres.baladeur.modulesocc as ia
        self.list_ia.append(ia)
        import autres.aatarek.RepoSoccer_master.prog as ia
        self.list_ia.append(ia)
        import autres.chefifarouck.FarouckYann as ia
        self.list_ia.append(ia)
        self.list_ia.append(m)
        

        self.my_get_features_1v1.__dict__["names"]= ["dist_ball","dist_but_ennemi","dist_ball_but_ennemi",
                                      "can_shoot", "ball_champs_def", "is_closer_ball","existe_adv_devant",
                                      "existe_gardien", "dist_ennemi"]        
    
        self.my_get_features_2v2.__dict__["names"]= ["dist_ball","dist_but_ennemi","dist_ball_but_ennemi",
                                      "can_shoot", "ball_champs_def", "is_closer_ball","existe_adv_devant",
                                      "existe_ami_devant", "existe_gardien", "dist_ami_devant",
                                          "dist_ennemi_devant", "dist_ami", "dist_ennemi"]    
    
    
    
    def entrainer_contre_tous(self, fname1, fname2 = None):
        if self.nb_players == 1:
            jouer = True
            while (jouer):
                nb_ia = input('Choose the ia : ')
                nb_ia = int(nb_ia)
                self.entrainer1v1_main(fname1, self.list_ia[nb_ia])
                keep_play = input ('Play again?')
                if keep_play == 'n':
                    jouer = False
        elif self.nb_players == 2:
            jouer = True
            while (jouer):
                nb_ia = input('Choose the ia : ')
                nb_ia = int(nb_ia)
                self.entrainer2v2_main(fname1, fname2, self.list_ia[nb_ia])
                keep_play = input ('Play again?')
                if keep_play == 'n':
                    jouer = False
            
        else:
            print("Not yet ready")
            
            
### Transformation d'un etat en features : state,idt,idp -> R^d

    def my_get_features_1v1(self, state, id_team, id_player):
        """ extraction du vecteur de features d'un etat, ici distance a la balle, distance au but, distance balle but... """
        tools = m.ToolBox(state,id_team,id_player)
        
        f1 = tools.VecPosBall().norm
        f2 = tools.VecPosGoal().norm
        f3 = tools.VecPosBallToGoal().norm 
    
        f4 = int(tools.CanShoot())
        f5 = int(tools.EstDef())
        f6 = int(tools.IsCloserToBall())
        f7 = int(tools.ExisteAdversaireDevant())        

        f8 = int(tools.AdvAGardien())
        
        f9 = tools.VecPosAdvPlusProche().norm
#        
#       
        return [f1, f2, f3, f4, f5, f6, f7, f8, f9]
        
        
    def my_get_features_2v2(self, state, id_team, id_player):
        """ extraction du vecteur de features d'un etat, ici distance a la balle, distance au but, distance balle but... """
        tools = m.ToolBox(state,id_team,id_player)
        
        f1 = tools.VecPosBall().norm
        f2 = tools.VecPosGoal().norm
        f3 = tools.VecPosBallToGoal().norm 
    
        f4 = int(tools.CanShoot())
        f5 = int(tools.EstDef())
        f6 = int(tools.IsCloserToBall())
        f8 = int(tools.ExisteAmiDevant())
        f7 = int(tools.ExisteAdversaireDevant())        
        f9 = int(tools.AdvAGardien())
        f10 = tools.VecPosAdvPlusProche().norm
        
                   
        if tools.VecPosAmisPlusProcheDevant() is None :
            f11 = -1
        else: 
            f11 = tools.VecPosAmisPlusProcheDevant().norm
        
        if tools.VecPosAdvPlusProcheDevant() is None :
            f12 = -1
        else:
            f12 = tools.VecPosAdvPlusProcheDevant().norm
    

        f13 = tools.VecPosAmisPlusProche().norm
            
        return [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13]
                

    
    def entrainer1v1_main(self, fname, ia):
        
        if self.nb_players != 1:
            raise Exception("Not the good number of players for this function.")
        
        #Creation d'une partie
        kb_strat = KeyboardStrategy()
        kb_strat.add("a", m.strategy.ShootStrat())
        kb_strat.add("z", m.strategy.DefStrat())
        kb_strat.add("e", m.strategy.GardienStrat())
        kb_strat.add("q", m.strategy.DribleStrat())
        kb_strat.add("s", m.strategy.PassStrat())
        kb_strat.add("d", m.strategy.AtkStrat())
        
        team1 = SoccerTeam(name="Control Team")
        #team2 = SoccerTeam(name="Sparing")
        team1.add("ControlPlayer",kb_strat)
        #team2.add("Player",m.strategy.ShootStrat()) 
        team2 = ia.get_team(1)
        simu = Simulation(team1,team2)
        #Jouer, afficher et controler la partie
        show_simu(simu)
        print("Nombre d'exemples : "+str(len(kb_strat.states)))
        
        # Sauvegarde des etats dans un fichier
        if simu.get_score_team(1) > simu.get_score_team(2):
            try: 
                temp = load_jsonz(fname)
                temp+= kb_strat.states
                dump_jsonz(temp,fname)
            except FileNotFoundError:
                dump_jsonz( kb_strat.states,fname)
                   
                
    def entrainer2v2_main(self, fname1, fname2, ia):
        
        if self.nb_players != 2:
            raise Exception("Not the good number of players for this function.")
        
        #Creation d'une partie
        kb_strat1 = KeyboardStrategy()
        kb_strat1.add("a", m.strategy.ShootStrat())
        kb_strat1.add("z", m.strategy.DefStrat())
        kb_strat1.add("e", m.strategy.GardienStrat())
        kb_strat1.add("q", m.strategy.DribleStrat())
        kb_strat1.add("s", m.strategy.PassStrat())
        kb_strat1.add("d", m.strategy.AtkStrat())
        
        kb_strat2 = KeyboardStrategy()
        kb_strat2.add("u", m.strategy.ShootStrat())
        kb_strat2.add("i", m.strategy.DefStrat())
        kb_strat2.add("o", m.strategy.GardienStrat())
        kb_strat2.add("j", m.strategy.DribleStrat())
        kb_strat2.add("k", m.strategy.PassStrat())
        kb_strat2.add("l", m.strategy.AtkStrat())
        
        team1 = SoccerTeam(name="Control Team")
        #team2 = SoccerTeam(name="Sparing")
        team1.add("ControlPlayer",kb_strat1)
        team1.add("ControlPlayer",kb_strat2)
        #team2.add("Player",m.strategy.ShootStrat()) 
        team2 = ia.get_team(2)
        simu = Simulation(team1,team2)
        #Jouer, afficher et controler la partie
        show_simu(simu)
        print("Nombre d'exemples : "+str(len(kb_strat1.states) + len(kb_strat2.states)))
        
        # Sauvegarde des etats dans un fichier
        if simu.get_score_team(1) >= simu.get_score_team(2):
            try: 
                temp_joueur_1 = load_jsonz(fname1)
                temp_joueur_1+= kb_strat1.states
                dump_jsonz(temp_joueur_1,fname1)
            except FileNotFoundError:
                dump_jsonz( kb_strat1.states,fname1)
            
            try: 
                temp_joueur_2 = load_jsonz(fname2)
                temp_joueur_2+= kb_strat2.states
                dump_jsonz(temp_joueur_2,fname2)
            except FileNotFoundError:
                dump_jsonz( kb_strat2.states,fname2)
    
    def apprendre_1v1(self, exemples, get_features_1v1,fname=None):
        #genere l'ensemble d'apprentissage
        data_train, data_labels = build_apprentissage(exemples,get_features_1v1)
        #Apprentissage de l'arbre
        dt = apprend_arbre(data_train,data_labels,depth=10, feature_names=get_features_1v1.names)
        ##Sauvegarde de l'arbre
        if fname is not None:
            with open(fname,"wb") as f:
                pickle.dump(dt,f)
        return dt
        
    def apprendre_2v2(self, exemples, get_features_2v2,fname=None):
        #genere l'ensemble d'apprentissage
        data_train, data_labels = build_apprentissage(exemples,get_features_2v2)
        #Apprentissage de l'arbre
        dt = apprend_arbre(data_train,data_labels,depth=10, feature_names=get_features2v2.names)
        ##Sauvegarde de l'arbre
        if fname is not None:
            with open(fname,"wb") as f:
                pickle.dump(dt,f)
        return dt
    
    def create_rd_state(self):
        state = SoccerState.create_initial_state(self.nb_players, self.nb_players)
          
        state.ball.position = Vector2D(rd.uniform(0, GAME_WIDTH), rd.uniform(0, GAME_HEIGHT))
        
        state.ball.vitesse = Vector2D(norm = rd.uniform(0, maxBallAcceleration), angle = rd.uniform(0, np.pi * 2)) 
        
        for i in range (self.nb_players):
        
            state.states[(1, i)].position = Vector2D(rd.uniform(0, GAME_WIDTH), rd.uniform(0, GAME_HEIGHT))  
            state.states[(1, i)].vitesse =  Vector2D(norm = rd.uniform(0, maxPlayerSpeed), angle = rd.uniform(0, np.pi * 2)) 
        
            state.states[(2, i)].position = Vector2D(rd.uniform(0, GAME_WIDTH), rd.uniform(0, GAME_HEIGHT))  
            state.states[(2, i)].vitesse =  Vector2D(norm = rd.uniform(0, maxPlayerSpeed), angle = rd.uniform(0, np.pi * 2)) 
        
        return state
        
    def affiche_rd_state(self, state, w = 1200, h = 800):
        gui = SimuGUI(width = w, height = h)
        gui.show(state)
        pyg_start()

    def entrainer2v2_snap(self, fname1, fname2, nb_snap):
        
        if self.nb_players != 2:
            raise Exception("Not the good number of players for this function.")
                
       #Creation d'une partie
        kb_strat1 = KeyboardStrategy()
        kb_strat1.add("a", m.strategy.ShootStrat())
        kb_strat1.add("z", m.strategy.DefStrat())
        kb_strat1.add("e", m.strategy.GardienStrat())
        kb_strat1.add("q", m.strategy.DribleStrat())
        kb_strat1.add("s", m.strategy.PassStrat())
        kb_strat1.add("d", m.strategy.AtkStrat())
        
        kb_strat2 = KeyboardStrategy()
        kb_strat2.add("a", m.strategy.ShootStrat())
        kb_strat2.add("z", m.strategy.DefStrat())
        kb_strat2.add("e", m.strategy.GardienStrat())
        kb_strat2.add("q", m.strategy.DribleStrat())
        kb_strat2.add("s", m.strategy.PassStrat())
        kb_strat2.add("d", m.strategy.AtkStrat())
        
        kb_strat2.idp = 1
        
        sortie = False
        i = 0
        
        while (not sortie) and i < nb_snap:
            
            state = self.create_rd_state()
            kb_strat1.state = state
            kb_strat2.state = state            
            self.affiche_rd_state(state, 900, 600)
            
            joueur_0 = input("Choose strategy for player red 0 : ")
            joueur_1 = input("Choose strategy for player red 1 : ")
            
            kb_strat1.send_strategy(joueur_0)
            kb_strat2.send_strategy(joueur_1)
            
            if input("wanna continue?" ) ==  "n":
                sortie = True
                
            i+=1
                
        try: 
            temp_joueur_1 = load_jsonz(fname1)
            temp_joueur_1+= kb_strat1.states
            dump_jsonz(temp_joueur_1,fname1)
        except FileNotFoundError:
            dump_jsonz( kb_strat1.states,fname1)
        try: 
            temp_joueur_2 = load_jsonz(fname2)
            temp_joueur_2+= kb_strat2.states
            dump_jsonz(temp_joueur_2,fname2)
        except FileNotFoundError:
            dump_jsonz( kb_strat2.states,fname2)
    
        
        
        
