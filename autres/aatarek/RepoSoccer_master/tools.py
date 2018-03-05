from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import Simulation, SoccerTeam, Player, show_simu
from soccersimulator import Strategy
from soccersimulator import settings
from soccersimulator import utils
from soccersimulator.settings import *
import random
import math

class functions(object):
	def __init__(self,state,id_team,id_player):
		self.state = state
		self.id_team = id_team
		self.id_player = id_player

	def vecteurShootGoal(self,Balle, cage_x, cage_y, puissance):
		return Vector2D((cage_x - Balle.position.x),(cage_y - Balle.position.y)).normalize() * puissance

	def teta2Vecteurs(self,v1, v2):
		teta = math.acos((v1.x*v2.x + v1.y*v2.y) / (v1.norm*v2.norm))
		return teta

	def idEnemy(self):
		goalX = 0
		if(self.id_team == 2):
			goalX = 1
		return goalX

	def playerData(self): 
		posx = self.state.player_state(self.id_team, self.id_player).position.x
		posy = self.state.player_state(self.id_team, self.id_player).position.y
		ballx = self.state.ball.position.x
		bally = self.state.ball.position.y
		return posx, posy, ballx, bally;

	def butPosition(self):
		goalX = 0
		goalY = GAME_HEIGHT / 2
		if (self.id_team == 1):
			goalX = GAME_WIDTH
		return goalX, goalY;

	def distBallJoueur(self):
		playerDataa = self.playerData()
		return math.hypot(playerDataa[2] - playerDataa[0], playerDataa[3] - playerDataa[1])

	def tirBoulet(self):
		return self.vecteurShootGoal(self.state.ball, self.butPosition()[0], self.butPosition()[1], 10)

	def canShoot(self):
		return self.distBallJoueur() < PLAYER_RADIUS + BALL_RADIUS 


	#def obstacle(Balle, cage_x, cage_y, puissance):
	#	tirVecteur = vecteurShootGoal(Balle, cage_x, cage_y, puissance)
	
