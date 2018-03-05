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
		self.nb_players = state.nb_players(1)


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

	#def cage(self):
	#	if self.id_team==1:
	#		return Vector2D(GAME_WIDTH,GAME_HEIGHT/2.)
	#	else:
	#		return Vector2D(0,GAME_HEIGHT/2.)

	def adv_le_plus_proche(self):
        	adv = 0
        	for i in range(self.nb_players):
            		if self.p_position.distance(self.state.player_state(self.id_adverse_team,i).position) < self.p_position.distance(self.state.player_state(self.id_adverse_team,adv).position):
                		adv = i
        	return self.state.player_state(self.id_adverse_team,adv).position

	def interception(self):
		playergauche = 0
		playerdroit = 0
		for i in range(self.nb_players):
			if self.state.player_state(self.id_adverse_team,i).position.x <= self.state.player_state(self.id_adverse_team,playergauche).position.x:
				playergauche = i
			if self.state.player_state(self.id_adverse_team,i).position.x > self.state.player_state(self.id_adverse_team,playerdroit).position.x:
				playerdroit = i
			return (self.state.player_state(self.id_adverse_team,playerdroit).position + self.state.player_state(self.id_adverse_team,playergauche).position)/2
