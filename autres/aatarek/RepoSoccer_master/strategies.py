from soccersimulator import *
from soccersimulator.settings import *
from .tools import *
import random
import math

## Strategie La flemme
class flemme(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Random")
	def compute_strategy(self,state,id_team,id_player):
		f = functions(state,id_team,id_player)
		idEnemy = f.idEnemy
		
		if(f.canShoot()):
				return SoccerAction(Vector2D(angle=3.14,norm=0.2), f.tirBoulet())
		elif ( f.playerData()[0] < (GAME_WIDTH - 11) ):
			return SoccerAction(f.tirBoulet())
		elif (state.step % 50 < 25):
			return SoccerAction(Vector2D(0,f.butPosition() + GAME_GOAL_HEIGHT / 2 - f.playerData()[1]).normalize() * (maxPlayerAcceleration / 2), Vector2D(0,0))
		else:
			return SoccerAction(Vector2D(0,f.butPosition() - GAME_GOAL_HEIGHT / 2 - f.playerData()[1]).normalize() * maxPlayerAcceleration, Vector2D(0,0))
	

## Strategie Attente puis But
class stratAttente(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Random")
	def compute_strategy(self,state,id_team,id_player):
		f = functions(state,id_team,id_player)
		idEnemy = f.idEnemy

		# Si la balle est au centre (engagement) on ne bouge pas
		if (state.ball.position.x == (GAME_WIDTH / 2) and state.ball.position.y == f.butPosition and state.step < 35):
			return SoccerAction(Vector2D(0,0), Vector2D(0,0))
		elif(f.canShoot()):
			return SoccerAction(Vector2D(angle=3.14,norm=0.2), f.tirBoulet())
		else:
			return SoccerAction(Vector2D(f.playerData()[2] - f.playerData()[0],f.playerData()[3] - f.playerData()[1]).normalize() * maxPlayerAcceleration, Vector2D(0,0))


