from soccersimulator import *
from soccersimulator.settings import *
from .tools import *
import random
import math

## Strategie defense 1
class defense(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Defense1")
	def compute_strategy(self,state,id_team,id_player):
		f = functions(state,id_team,id_player)
		return f.defense()

## Strategie defense 2
class defense2(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Defense2")
	def compute_strategy(self,state,id_team,id_player):
		f = functions(state,id_team,id_player)
		return f.defense2()


## Strategie Attente puis But
class stratAttente(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Attack1")
	def compute_strategy(self,state,id_team,id_player):
		f = functions(state,id_team,id_player)
		return f.attack()



