from profAI import ParamSearch
from profAI import FonceurTestStrategy
from soccersimulator import Strategy, SoccerAction, Vector2D
from soccersimulator import SoccerTeam, Simulation
from soccersimulator import show_simu
from module.strategie import Fonceur
from module.strategie import Fonceur_brain_opti
from module.strategie import Fonceur_brain
from module.strategie import RandomStrategy
from module.strategie import Defenseur
from module.strategie import Defenseur_2v2
from module.strategie import Defenseur_2v2_opti
from module.strategie import Bon_joueur_1v1
from module.strategie import Bon_joueur_2v2
from numpy import arange


expe = ParamSearch(strategy=Defenseur_2v2_opti(),
                   params={'cst_defense': arange(0,0.25, 0.01)},max_round_step=200)
expe.start(show=False)
print(expe.get_res())

l = expe.get_res()
maxi=0
mini=20

for cle in l.keys():
    if l[cle] >= maxi:
        maxi = l[cle]
print(maxi)
for a in l.keys():
    if l[a] == maxi:
        print("max", a, maxi)

for cle in l.keys():
    if l[cle] <= mini:
        mini = l[cle]
print(mini)
for a in l.keys():
    if l[a] == mini:
        print("min", a, mini)

## (cst_dribble_B, cst_dribble_A) = (32, 16): 0.7
## expe = ParamSearch(strategy=Fonceur_brain_opti(),
##		   params={'cst_dribble_A': arange(14,18, 0.5),
##			   'cst_dribble_B': arange(30,34, 0.5)},max_round_step=200)
## (cst_dribble_B, cst_dribble_A) = (31, 16.5): 0.7
## (cst_dribble_B, cst_dribble_A) = (32.5, 15.0): 0.7
## (cst_dribble_B, cst_dribble_A) = (32.5, 16.5): 0.7


## (cst_dribble_B, cst_dribble_A) = (44, 18): 0.7
## expe = ParamSearch(strategy=Fonceur_brain_opti(),
##		   params={'cst_dribble_A': arange(16,20, 0.5),
##			   'cst_dribble_B': arange(42,46, 0.5)},max_round_step=200)
## (cst_dribble_B, cst_dribble_A) = (42.5, 17.0): 0.7
## (cst_dribble_B, cst_dribble_A) = (44.0, 18.5): 0.8


