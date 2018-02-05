# -*- coding: utf-8 -*-
from soccersimulator import ChallengeFonceurButeur, SoccerTeam, show_simu
from module import *

import numpy as np
import matplotlib.pyplot as plt

accFirst = np.arange(0.5, 1.0, 0.01)
accOther = np.arange(0.5, 1.0, 0.01)

accFirst, accOther = np.meshgrid(accFirst, accOther)

time = np.empty_like(accFirst)

for i in range(time.shape[0]):
    for j in range(time.shape[1]):
        print("accFirst =",accFirst[i, j],"accOther =",accOther[i, j])
        
        team = SoccerTeam("Equipe")
        team.add("Joueur",ShootBallStrategyTwoAccelerations(accFirst[i, j], accOther[i, j]))
        
        challenge = ChallengeFonceurButeur(team,max_but=10, max_steps = float("inf"))
        challenge.start()
        #print("temps moyen : ",challenge.stats_score, "\nliste des temps",challenge.resultats)
        time[i, j] = challenge.stats_score
    
amin = time.argmin()
amin = np.unravel_index(amin, time.shape)
print("Minimum: i =",amin[0],"j =",amin[1],"\n accFirst =",accFirst[amin[0], amin[1]],"accOther =",accOther[amin[0], amin[1]], "\ntime =",time[amin[0], amin[1]])

plt.contourf(accFirst, accOther, time, 50)
plt.xlabel('accFirst')
plt.ylabel("accOther")
plt.colorbar()

# Conclusion :
## accFirst optimal vaut 0.64, comme dans le cas des tirs avec la même accéleration.
## Plusieurs valeurs pour accOther donnent un temps minimal de 119.9:
## accOther = 0.52, 0.60, 0.65, 0.71, ...
## On arrive à la conclusion que ça ne vaut pas la peine de changer l'accéleration
## entre le premier et le deuxième tir.