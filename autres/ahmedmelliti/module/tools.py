from soccersimulator  import Strategy, SoccerAction, Vector2D, SoccerState
from soccersimulator import SoccerTeam, Simulation, Player
from soccersimulator import show_simu
from soccersimulator.settings import *


class Tools(object):
	def __init__(self, state,id_team,id_player):
		self.state = state
		self.id_team = id_team
		self.id_player= id_player

		if self.id_team == 2:
			self.id_adverse_team = 1
		else:
			self.id_adverse_team = 2
		
		if self.id_team ==1:
			self.cage = Vector2D(0,GAME_HEIGHT/2.)
			self.cage_adv = Vector2D(GAME_WIDTH,GAME_HEIGHT/2.) 
		else:
			self.cage = Vector2D(GAME_WIDTH,GAME_HEIGHT/2.)
			self.cage_adv = Vector2D(0,GAME_HEIGHT/2.)

		self.ball_position = self.state.ball.position
		self.ball_vitesse = self.state.ball.vitesse
		self.p_position = self.state.player_state(id_team,id_player).position
		self.vitesse = self.state.player_state(self.id_team,self.id_player).vitesse	
		self.nb_players = state.nb_players(1)

		if self.nb_players >= 2:
			if self.id_player == 1:
				self.ami_position = self.state.player_state(self.id_team,0).position
			else:
				self.ami_position = self.state.player_state(self.id_team,1).position

	def goto(self, position):
		return (position-self.state.player_state(self.id_team,self.id_player).position)

	def shoot(self, position):
		return (position-self.state.player_state(self.id_team,self.id_player).position)
		
	#def dbp(self):
	#	return self.state.player_state(self.id_team,self.id_player).position.distance(self.state.ball.position)
	def dbp(self):
		return self.p_position.distance(self.ball_position)


	def canshoot(self):
		return self.dbp()>=PLAYER_RADIUS+BALL_RADIUS

	def canshoot1(self):
		if (self.p_position.distance(self.ball_position) < (PLAYER_RADIUS + BALL_RADIUS)):
			return True
		return False 

	def adv_le_plus_proche(self):
		adv = 0
		for i in range(self.nb_players):
			if self.p_position.distance(self.state.player_state(self.id_adverse_team,i).position) < self.p_position.distance(self.state.player_state(self.id_adverse_team,adv).position):
				adv = i
		return self.state.player_state(self.id_adverse_team,adv).position

	def adv_le_plus_proche_vitesse(self):
		adv = 0
		for i in range(self.nb_players):
			if self.p_position.distance(self.state.player_state(self.id_adverse_team,i).position) < self.p_position.distance(self.state.player_state(self.id_adverse_team,adv).position):
				adv = i
		return self.state.player_state(self.id_adverse_team,adv).vitesse

	def interception(self):
		playergauche = 0
		playerdroit = 0
		for i in range(self.nb_players):
			if self.state.player_state(self.id_adverse_team,i).position.x <= self.state.player_state(self.id_adverse_team,playergauche).position.x:
				playergauche = i
			if self.state.player_state(self.id_adverse_team,i).position.x > self.state.player_state(self.id_adverse_team,playerdroit).position.x:
				playerdroit = i
			return (self.state.player_state(self.id_adverse_team,playerdroit).position + self.state.player_state(self.id_adverse_team,playergauche).position)/2

	def joueur_position_shoot(self):
		return self.p_position.distance(self.cage_adv)<GAME_WIDTH/3.
	
	def shoot1(self,p):
		return SoccerAction(Vector2D(),p.normalize()*4.6)
	
	def shoot_cage(self):
		return self.shoot1(self.cage_adv-self.ball_position)
	
	def dribble(self):
		a = self.cage_adv-self.ball_position
		a = a.normalize()*1.68
		return SoccerAction(Vector2D(),a)

	def passe(self):
		return self.shoot1(self.ami_position - self.p_position)

	def au_milieu(self):
		return self.cage.distance(self.p_position)<GAME_WIDTH/2.

	def au_cage(self):
		return self.cage.distance(self.p_position)<GAME_WIDTH/4.

	def en_attaque(self):
		return self.cage.distance(self.p_position)<GAME_WIDTH*2/3.

	def ball_avant_adv(self):
		return self.p_position.distance(self.ball_position + self.vitesse) < self.p_position.distance(self.adv_le_plus_proche() + self.adv_le_plus_proche_vitesse())
	
	def ball_avant_adv_avc(self):
		return self.p_position.distance(self.ball_position + self.vitesse) < self.p_position.distance(self.adv_le_plus_proche() + self.adv_le_plus_proche_vitesse())+20
