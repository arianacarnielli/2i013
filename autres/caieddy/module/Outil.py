from soccersimulator import Strategy, SoccerAction, Vector2D
from soccersimulator import SoccerTeam, Simulation
from soccersimulator import show_simu
from soccersimulator.settings import *


class Outil(object):
	def __init__(self,state,team,player, force=1):
		self.state=state
		self.team=team
		self.player=player
		self.force = force
	def goal_team(self):
		if (self.team == 1):
			return (0,GAME_HEIGHT/2)
		return (GAME_WIDTH, GAME_HEIGHT/2)
		
	def vitesse_ball(self):
		return self.state.ball.vitesse	
	def posi_ball(self):
		return self.state.ball.position
	def posi_player(self):
		return self.state.player_state(self.team,self.player).position 
	def dist_player_ball(self):
		return (self.posi_ball() - self.posi_player()).norm
	def vect_player_ball(self):
		return (self.posi_ball() - self.posi_player())
	def peut_tirer(self):
		if (self.dist_player_ball() < PLAYER_RADIUS + BALL_RADIUS):
			return True
		return False

	def vect_player_posi(self,x,y):
		return Vector2D(x,y) - self.posi_player()

	def revenir_posi_def(self,id_team):
		if (id_team == 1):
			return SoccerAction(self.vect_player_posi(GAME_WIDTH*1/8,(((self.posi_ball().y)- (GAME_HEIGHT/2))/self.posi_ball().x)*(GAME_WIDTH*1/8) + GAME_HEIGHT/2),0)
		return SoccerAction(self.vect_player_posi(GAME_WIDTH*7/8,((((self.posi_ball().y)- (GAME_HEIGHT/2))/((self.posi_ball().x) - (GAME_WIDTH)))*(GAME_WIDTH*7/8) + GAME_HEIGHT/2 - (((self.posi_ball().y)- (GAME_HEIGHT/2))/((self.posi_ball().x)-(GAME_WIDTH)))*GAME_WIDTH)),0)

	def revenir_posi_counter(self,id_team):
		if (self.posi_adversaire().y < GAME_HEIGHT/2):
			return SoccerAction(self.vect_player_posi((GAME_WIDTH)*1/2,(GAME_HEIGHT)*3/4),0)
		return SoccerAction(self.vect_player_posi((GAME_WIDTH)*1/2,(GAME_HEIGHT)*1/4),0)
		


	
	def ball_dans_rayon_but(self, id_team):
		if (id_team == 1):
			return self.posi_ball().x < (GAME_WIDTH)*2/5
		return self.posi_ball().x > (GAME_WIDTH)*3/5


	def defendre(self, id_team):
		return SoccerAction(self.vect_player_ball(),self.renvoyer_ball(id_team))

	def renvoyer_ball(self, id_team):
		if (id_team ==1):
			return self.vect_player_posi(GAME_WIDTH,(GAME_HEIGHT)*1/2)
		return self.vect_player_posi(0,(GAME_HEIGHT)*1/2)


	def bonne_precision(self,id_team):
		if (id_team == 1):
			return (Vector2D(GAME_WIDTH,GAME_HEIGHT/2) - self.posi_ball())/8
		return (Vector2D(0,GAME_HEIGHT/2) - self.posi_ball())/8
	def mauvaise_precision(self,id_team):
		if (id_team == 1):
			return (Vector2D(GAME_WIDTH,GAME_HEIGHT/2) - self.posi_ball())/40
		return (Vector2D(0,GAME_HEIGHT/2) - self.posi_ball())/40
		

	def tir_bonne_precision(self,id_team):
		return SoccerAction(self.vect_player_ball(),self.bonne_precision(id_team))
	def tir_mauvaise_precision(self,id_team):
		return SoccerAction(self.vect_player_ball(),self.mauvaise_precision(id_team))


	def tir(self, id_team):
		if (id_team == 1):
			if (self.posi_ball().x > (GAME_WIDTH*3/4)):
				return self.tir_bonne_precision(id_team)
			return self.tir_mauvaise_precision(id_team)
		if (id_team == 2):
			if (self.posi_ball().x < (GAME_WIDTH*1/4)):
				return self.tir_bonne_precision(id_team)
			return self.tir_mauvaise_precision(id_team)


	def courir_vers_ball(self):
		return SoccerAction(self.vect_player_ball(),0)
		
	def courir_vers_ball_predi(self):
		return SoccerAction(self.vect_player_posi(self.predire_la_balle().x,self.predire_la_balle().y),0)

	def predire_la_balle(self):
		Constante = 0.6*self.dist_player_ball()
		return self.posi_ball() + Constante*self.vitesse_ball()

	def rien_faire(self):
		return SoccerAction(0,0)


	def posi_adversaire(self):
		idteam = 1 if self.team == 2 else 2
		return self.state.player_state(idteam,0).position

	def adversaire_devant_player_haut(self,id_team):
		if (id_team == 1):
			if (self.posi_player().x < self.posi_adversaire().x):
				if (self.posi_player().y < self.posi_adversaire().y):
					return True
			return False
		if (id_team == 2):
			if (self.posi_player().x > self.posi_adversaire().x):
				if (self.posi_player().y < self.posi_adversaire().y):
					return True
			return False	


	def adversaire_devant_player_bas(self,id_team):
		if (id_team == 1):
			if (self.posi_player().x < self.posi_adversaire().x):
				if (self.posi_player().y > self.posi_adversaire().y):
					return True
			return False
		if (id_team == 2):
			if (self.posi_player().x > self.posi_adversaire().x):
				if (self.posi_player().y > self.posi_adversaire().y):
					return True
			return False


	def tir_vers_milieu_bas(self):
		return SoccerAction(self.vect_player_ball(), (Vector2D((GAME_WIDTH)*1/2,(GAME_HEIGHT)*1/4) - self.posi_ball())/60)

	def tir_vers_milieu_haut(self):
		return SoccerAction(self.vect_player_ball(), (Vector2D((GAME_WIDTH)*1/2,(GAME_HEIGHT)*3/4) - self.posi_ball())/60)



	def tir_vers_milieu_bas_def(self):
		return SoccerAction(self.vect_player_ball(), (Vector2D((GAME_WIDTH)*1/2,(GAME_HEIGHT)*1/4) - self.posi_ball())/8)

	def tir_vers_milieu_haut_def(self):
		return SoccerAction(self.vect_player_ball(), (Vector2D((GAME_WIDTH)*1/2,(GAME_HEIGHT)*3/4) - self.posi_ball())/8)


	def peut_jouer(self):
		if (self.dist_player_ball() < 50):
			return True
		return False

	def recuperation_ball_pret(self):
		if (self.dist_player_ball() < 10):
			return True
		return False

	def attaque_fonceur(self,id_team):
		if (self.peut_tirer()):
			return self.tir(id_team)
		return self.courir_vers_ball_predi()

	def defense(self,id_team):
		if (self.ball_dans_rayon_but(id_team)):
			if (self.peut_tirer()):
				return self.defendre(id_team)
			return self.courir_vers_ball_predi()
		else:
			return self.revenir_posi_def(id_team)

			
	def defense_2v2(self,id_team):
		if (self.ball_dans_rayon_but(id_team)):
			if (self.adversaire_devant_player_haut(id_team)):
				if (self.peut_tirer()):
					return self.tir_vers_milieu_bas_def()
				return self.courir_vers_ball_predi()
			if (self.adversaire_devant_player_bas(id_team)):
				if (self.peut_tirer()):
					return self.tir_vers_milieu_haut_def()
				return self.courir_vers_ball_predi()
			
		return self.revenir_posi_def(id_team)


	def dribbler_1v1(self,id_team):
		if (self.peut_jouer()):
			if (self.adversaire_devant_player_haut(id_team)):
				if (self.peut_tirer()):
					print("tir_vers_milieu_bas")
					return self.tir_vers_milieu_bas()
				print("courir_vers_ball_predi")
				return self.courir_vers_ball_predi()
			if (self.adversaire_devant_player_bas(id_team)):
				if (self.peut_tirer()):
					print("tir_vers_milieu_haut")
					return self.tir_vers_milieu_haut()
				print("courir_vers_ball_predi")
				return self.courir_vers_ball_predi()
			print("attaque_fonceur")
			return self.attaque_fonceur(id_team)
		print("revennir_posi_attaquant")
		return self.revenir_posi_attaquant(id_team)


	def revenir_posi_attaquant(self,id_team):
		if (id_team == 1):
			return SoccerAction(self.vect_player_posi((GAME_WIDTH)*1/8,(GAME_HEIGHT)*1/2),0)
		return SoccerAction(self.vect_player_posi((GAME_WIDTH)*7/8,(GAME_HEIGHT)*1/2),0)


	def ball_devant_player(self,id_team):
		if (id_team == 1):
			if (self.posi_player().x < self.posi_ball().x):
				return True
			return False
		if (self.posi_player().x > self.posi_ball().x):
			return True
		return False
















