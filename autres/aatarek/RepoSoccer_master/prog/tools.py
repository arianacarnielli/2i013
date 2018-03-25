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

	def ShootOuAvanceVersBalle(self):
		if (self.canShoot()):
			return self.TirDirect()
		else:
			return self.AvanceVersBalle()

	def BougePas(self):
		return SoccerAction(Vector2D(0,0), Vector2D(0,0))

		
	def AvanceVersBalle(self):
		return SoccerAction(Vector2D(self.playerData()[2] - self.playerData()[0],self.playerData()[3] - self.playerData()[1]).normalize() * maxPlayerAcceleration, Vector2D(0,0))

	def TirDirect(self):
		return SoccerAction(Vector2D(angle=3.14,norm=0.2), self.tirBoulet())

	def Ralenti(self):
		return SoccerAction(Vector2D(angle=0,norm=0.001), Vector2D(0,0))
	
	def Team2(self):
		return self.id_team == 2

	def Team1(self):
		return self.id_team == 1
	
	def Ballx2sup(self):
		return self.state.ball.position.x > (GAME_WIDTH / 2) 

	def Ballx2inf(self):
		return self.state.ball.position.x < (GAME_WIDTH / 2)

	def Ballx4sup(self):
		return self.state.ball.position.x > (3*GAME_WIDTH / 4)

	def Ballx4inf(self):
		return self.state.ball.position.x < (GAME_WIDTH / 4)


	def defense(self):
		if self.Team2():
			if self.Ballx2sup():
				return self.ShootOuAvanceVersBalle()
			else:
				return self.Ralenti()
		else:
			if self.Ballx2inf():
				return self.ShootOuAvanceVersBalle()
			else:
				return self.Ralenti()

	def defense2(self):
		if self.Team2():
			if self.Ballx4sup():
				return self.ShootOuAvanceVersBalle()
			else:
				return self.Ralenti()
		else:
			if self.Ballx4inf():
				return self.ShootOuAvanceVersBalle()
			else:
				return self.Ralenti()
	
	def attack(self):
		if(self.canShoot()):
			return self.TirDirect()
		else:
			if self.Team2() and (self.id_player == 1) and self.Ballx2sup():
				return self.BougePas()
			elif self.Team1() and (self.id_player == 1) and self.Ballx2inf():
				return self.BougePas()
			elif self.Team1() and (self.id_player == 2) and self.Ballx4sup() and (playerDataa[0]>3*GAME_WIDTH / 4):
				return self.BougePas()
			elif self.Team2() and (self.id_player == 2) and self.Ballx4inf() and (playerDataa[0]<GAME_WIDTH / 4):
				return self.BougePas()
			else:
				return self.AvanceVersBalle()
	#def obstacle(Balle, cage_x, cage_y, puissance):
	#	tirVecteur = vecteurShootGoal(Balle, cage_x, cage_y, puissance)
	
