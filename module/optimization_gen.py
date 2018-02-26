# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 17:41:23 2018

@author: 3525837
"""

from __future__ import print_function, division
from soccersimulator import SoccerTeam, Simulation, Strategy, show_simu, Vector2D
from soccersimulator.settings import *

from .action import *
from .toolbox import *
from .strategy import *
from .comportement import *

import random as rd
import math


                
def genVectAleaStratDribleur():
    accShoot = rd.randrange(0, 10, 1) / 10.
    accDrible = rd.randrange(0, 10, 1) / 10.
    vit = rd.randrange(0, 10, 1) / 10.
    n = rd.randrange(0, 20, 1)
    maxAngle = round(rd.uniform(0, math.pi/2), 2)
    tooFar = rd.randrange(0, 60, 1)
    
    return [accShoot, accDrible, vit, n, maxAngle, tooFar]


class ParamSearch_gen(object):
    def __init__(self, strategy, params, simu=None, trials=20, max_steps=1000000,
                 max_round_step=40):
        self.strategy = strategy
        self.params = params.copy()
        self.simu = simu
        self.trials = trials
        self.max_steps = max_steps
        self.max_round_step = max_round_step

    def start(self, show=True):
        if not self.simu:
            team1 = SoccerTeam("Opt")
            team2 = SoccerTeam("Team 2")
            team1.add(self.strategy.name, self.strategy)
            team1.add(Strategy().name, Strategy())
            team2.add(Strategy().name, Strategy())
            self.simu = Simulation(team1, team2, max_steps=self.max_steps)
        self.simu.listeners += self

        if show:
            show_simu(self.simu)
        else:
            self.simu.start()

    def begin_match(self, team1, team2, state):
        self.last = 0  # Step of the last round
        self.crit1 = 0  # Criterion 1 to maximize (here, number of goals by team 1)
        self.crit2 = 0  # Criterion 2 to maximize (here, number of goals by team 2)
        self.cpt = 0  # Counter for trials

        if len(self.params) > 2:
            raise ValueError('Max two parameters')
        self.param_keys = list(self.params.keys())  # Name of all parameters
        self.param_id = [0] * len(self.param_keys)  # Index of the parameter values
        self.res = dict() # Dictionary of results

    def begin_round(self, team1, team2, state):
        ball = Vector2D(x = rd.uniform(GAME_WIDTH/4, 3*GAME_WIDTH/4), y = rd.uniform(0, GAME_HEIGHT))

        # Player and ball postion (random)
        self.simu.state.states[(1, 0)].position = Vector2D(x = rd.uniform(0, GAME_WIDTH/2), y = rd.uniform(0, GAME_HEIGHT))
        self.simu.state.states[(1, 1)].position = Vector2D(x = rd.uniform(GAME_WIDTH/2, GAME_WIDTH), y = rd.uniform(0, GAME_HEIGHT))
        self.simu.state.states[(2, 0)].position = Vector2D(x = rd.uniform(GAME_WIDTH/2, GAME_WIDTH), y = rd.uniform(0, GAME_HEIGHT))  # Player position
        #self.simu.state.states[(2, 0)].vitesse = Vector2D()  # Player acceleration
        self.simu.state.ball.position = ball.copy()  # Ball position
        self.simu.state.ball.vitesse = Vector2D(angle = rd.uniform(0, 2*math.pi), norm = rd.uniform(0, maxBallAcceleration))

        # Last step of the game
        self.last = self.simu.step

        # Set the current value for the current parameter
        for i, (key, values) in zip(self.param_id, self.params.items()):
            setattr(self.strategy, key, values[i])

    def update_round(self, team1, team2, state):
        # Stop the round if it is too long
        if state.step > self.last + self.max_round_step:
            self.simu.end_round()

    def end_round(self, team1, team2, state):
        # A round ends when there is a goal
        if state.goal == 1:
            self.crit1 += 1  # Increment criterion
        elif state.goal == 2:
            self.crit2 += 1

        self.cpt += 1  # Increment number of trials
        
        for i, (key, values) in zip(self.param_id, self.params.items()):
            print("{}: {}".format(key, values[i]), end="   ")
        print("Crit1: {}  Crit2: {}  Cpt: {}".format(self.crit1, self.crit2, self.cpt))
        
        if self.cpt >= self.trials:
            # Save the result
            res_key = tuple()
            for i, values in zip(self.param_id, self.params.values()):
                res_key += values[i],
            self.res[res_key] = [self.crit1 * 1. / self.trials, self.crit2 * 1. / self.trials]
            print(res_key, [self.crit1, self.crit2])

            # Reset parameters
            self.crit1 = 0
            self.crit2 = 0
            self.cpt = 0

            # Go to the next parameter value to try
            key0 = self.param_keys[0]
            if self.param_id[0] < len(self.params[key0]) - 1:
                self.param_id[0] += 1
            elif len(self.params) > 1:
                key1 = self.param_keys[1]
                if self.param_id[1] < len(self.params[key1]) - 1:
                    self.param_id[0] = 0
                    self.param_id[1] += 1
                else:
                    self.simu.end_match()
            else:
                self.simu.end_match()


    def get_res(self):
        return self.res



#### pas important ####
