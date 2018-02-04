# -*- coding: utf-8 -*-
from soccersimulator import ChallengeFonceurButeur, SoccerTeam, show_simu
from strategy import *

import numpy as np
import matplotlib.pyplot as plt

acc = np.arange(0.5, 1.0, 0.01)
time = np.empty_like(acc)

for i in range(acc.size):
    print("acc =",acc[i])
    
    team = SoccerTeam("Equipe")
    team.add("Joueur",ShootBallStrategy(acc[i]))
    
    challenge = ChallengeFonceurButeur(team,max_but=10, max_steps = float("inf"))
    challenge.start()
    #print("temps moyen : ",challenge.stats_score, "\nliste des temps",challenge.resultats)
    time[i] = challenge.stats_score
    
plt.plot(acc, time)
plt.xlabel('acceleration')
plt.ylabel("temps")
plt.grid(True)