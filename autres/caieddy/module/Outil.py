from soccersimulator import Strategy, SoccerAction, Vector2D
from soccersimulator import SoccerTeam, Simulation
from soccersimulator import show_simu
from soccersimulator.settings import *


class Outil(object):
	def __init__(self,state,team,player,cst_dribble_A=19.5, cst_dribble_B=22, cst_defense=0.11, cst_prediction=0.6):
		self.state=state
		self.team=team
		self.player=player
		self.cst_dribble_A = cst_dribble_A
		self.cst_dribble_B = cst_dribble_B
		self.cst_defense = cst_defense
		self.cst_prediction = cst_prediction
	def goal_team(self):
		if (self.team == 1):
			return (0,GAME_HEIGHT/2)
		return (GAME_WIDTH, GAME_HEIGHT/2)
		
	def idiot1(self):
		return SoccerAction(self.vect_player_posi((GAME_WIDTH)*1/4,(GAME_HEIGHT)*1/2),0)

	def idiot2(self):
		return SoccerAction(self.vect_player_posi((GAME_WIDTH)*1/10,(GAME_HEIGHT)*1/2),0)
	
	def idiot3(self):
		return SoccerAction(self.vect_player_posi((GAME_WIDTH)*1/15,(GAME_HEIGHT)*1/2),0)


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
		
	def dist_adversaire_player(self,adversaire):
		return (self.vect_player_posi(adversaire.x,adversaire.y).norm)
		

	def vect_player_posi(self,x,y):
		return Vector2D(x,y) - self.posi_player()

	def revenir_posi_def(self,id_team):
		if (id_team == 1):
			return SoccerAction(self.vect_player_posi(GAME_WIDTH*self.cst_defense,(((self.posi_ball().y)- (GAME_HEIGHT/2))/self.posi_ball().x)*(GAME_WIDTH*self.cst_defense) + GAME_HEIGHT/2),0)
		return SoccerAction(self.vect_player_posi(GAME_WIDTH - (self.cst_defense*GAME_WIDTH),((((self.posi_ball().y)- (GAME_HEIGHT/2))/((self.posi_ball().x) - (GAME_WIDTH)))*(GAME_WIDTH - (self.cst_defense*GAME_WIDTH)) + GAME_HEIGHT/2 - (((self.posi_ball().y)- (GAME_HEIGHT/2))/((self.posi_ball().x)-(GAME_WIDTH)))*GAME_WIDTH)),0)

	def revenir_posi_counter(self,id_team):
		if (self.adversaire_plus_proche_derriere().y < GAME_HEIGHT/2):
			return SoccerAction(self.vect_player_posi((GAME_WIDTH)*1/2,(GAME_HEIGHT)*3/4),0)
		return SoccerAction(self.vect_player_posi((GAME_WIDTH)*1/2,(GAME_HEIGHT)*1/4),0)
		


	
	def ball_dans_rayon_but(self, id_team):
		if (id_team == 1):
			return self.posi_ball().x < (GAME_WIDTH)*2/5
		return self.posi_ball().x > (GAME_WIDTH)*3/5


	def defendre(self, id_team):
		return SoccerAction(self.prediction_ball(),self.renvoyer_ball(id_team))

	def renvoyer_ball(self, id_team):
		if (id_team ==1):
			return self.vect_player_posi(GAME_WIDTH,(GAME_HEIGHT)*1/2)
		return self.vect_player_posi(0,(GAME_HEIGHT)*1/2)


	def bonne_precision(self,id_team):
		if (id_team == 1):
			return (Vector2D(GAME_WIDTH,GAME_HEIGHT/2) - self.posi_ball())/10
		return (Vector2D(0,GAME_HEIGHT/2) - self.posi_ball())/10
	def mauvaise_precision(self,id_team):
		if (id_team == 1):
			return (Vector2D(GAME_WIDTH,GAME_HEIGHT/2) - self.posi_ball())/60
		return (Vector2D(0,GAME_HEIGHT/2) - self.posi_ball())/60
		

	def tir_bonne_precision(self,id_team):
		return SoccerAction(self.prediction_ball(),self.bonne_precision(id_team))
	def tir_mauvaise_precision(self,id_team):
		return SoccerAction(self.prediction_ball(),self.mauvaise_precision(id_team))


	def tir(self, id_team):
		if (id_team == 1):
			if (self.posi_ball().x > (GAME_WIDTH*3/4)):
				return self.tir_bonne_precision(id_team)
			return self.tir_mauvaise_precision(id_team)
		if (id_team == 2):
			if (self.posi_ball().x < (GAME_WIDTH*1/4)):
				return self.tir_bonne_precision(id_team)
			return self.tir_mauvaise_precision(id_team)


	def courir_vers_ball_predi(self):
		return SoccerAction(self.prediction_ball(),0)
	

	def prediction_ball(self):
		return self.vect_player_posi(self.predire_la_balle().x,self.predire_la_balle().y)


	def predire_la_balle(self):
		Constante = self.cst_prediction*self.dist_player_ball()
		return self.posi_ball() + Constante*self.vitesse_ball()


	def rien_faire(self):
		return SoccerAction(0,0)
	
	def liste_amis(self):
		return [self.state.player_state(idteam, idplayer).position for idteam, idplayer in self.state.players if idteam == self.team and idplayer != self.id_player]

	def liste_adversaire(self):
        	return [self.state.player_state(idteam, idplayer).position for idteam, idplayer in self.state.players if idteam != self.team]


	def devant_nous(self, player2):
        	player1 = self.posi_player()
        	return (player2.x > player1.x and self.team == 1) or (player2.x < player1.x and self.team == 2)
	
	def derriere_nous(self, player2):
        	player1 = self.posi_player()
        	return (player2.x < player1.x and self.team == 1) or (player2.x > player1.x and self.team == 2)

	def au_dessu_nous(self, player2):
        	player1 = self.posi_player()
        	if player2.y > player1.y:
        		return True
        	return False
	
	def en_dessou_nous(self, player2):
        	player1 = self.posi_player()
        	if player2.y < player1.y:
        		return True
        	return False

	def adversaire_devant_player(self):
        	liste = self.liste_adversaire()
        	for i in liste:
            		if self.devant_nous(i):
                		return True
        	return False
	
	def adversaire_plus_proche_devant(self):
		liste = self.liste_adversaire()
		dist = GAME_WIDTH * 2
		adversaire = liste[0]
		for i in liste:
			a = self.dist_adversaire_player(i)
			if ((a < dist) & self.devant_nous(i)):
				adversaire = i
				dist = a
		return adversaire
	
	def adversaire_plus_proche_derriere(self):
		liste = self.liste_adversaire()
		dist = GAME_WIDTH * 2
		adversaire = liste[0]
		for i in liste:
			a = self.dist_adversaire_player(i)
			if ((a < dist) & self.derriere_nous(i)):
				adversaire = i
				dist = a
		return adversaire

	def ami_devant_player(self):
        	liste = self.liste_ami()
        	for i in liste:
            		if self.devant_nous(i):
                		return True
        	return False


	def tir_vers_milieu_bas(self):
		return SoccerAction(self.prediction_ball(), (Vector2D((GAME_WIDTH)*1/2,(GAME_HEIGHT)*1/4) - self.posi_ball())/60)
	def tir_vers_milieu_haut(self):
		return SoccerAction(self.prediction_ball(), (Vector2D((GAME_WIDTH)*1/2,(GAME_HEIGHT)*3/4) - self.posi_ball())/60)



	def tir_vers_milieu_bas_def(self):
		return SoccerAction(self.prediction_ball(), (Vector2D((GAME_WIDTH)*1/2,(GAME_HEIGHT)*1/4) - self.posi_ball())/8)
	def tir_vers_milieu_haut_def(self):
		return SoccerAction(self.prediction_ball(), (Vector2D((GAME_WIDTH)*1/2,(GAME_HEIGHT)*3/4) - self.posi_ball())/8)


	def peut_jouer(self):
		if (self.dist_player_ball() < 50):
			return True
		return False


	def recuperation_ball_pret(self):
		if (self.dist_player_ball() < 15):
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
			if (self.adversaire_devant_player() & self.au_dessu_nous(self.adversaire_plus_proche_devant())):
				if (self.peut_tirer()):
					return self.tir_vers_milieu_bas_def()
				return self.courir_vers_ball_predi()
			if (self.adversaire_devant_player() & self.en_dessou_nous(self.adversaire_plus_proche_devant())):
				if (self.peut_tirer()):
					return self.tir_vers_milieu_haut_def()
				return self.courir_vers_ball_predi()
			
		return self.revenir_posi_def(id_team)


	def dribbler_1v1(self,id_team):
		if (self.peut_jouer()):
			if (self.adversaire_devant_player() & self.au_dessu_nous(self.adversaire_plus_proche_devant())):
				if (self.peut_tirer()):
					return self.tir_vers_milieu_bas()
				return self.courir_vers_ball_predi()
			if (self.adversaire_devant_player() & self.en_dessou_nous(self.adversaire_plus_proche_devant())):
				if (self.peut_tirer()):
					return self.tir_vers_milieu_haut()
				return self.courir_vers_ball_predi()
			return self.attaque_fonceur(id_team)
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
		
		
	def fonceur_brain(self,id_team):
		if (id_team == 2):
			if (self.adversaire_devant_player() & self.en_dessou_nous(self.adversaire_plus_proche_devant()) & (self.dist_adversaire_player(self.adversaire_plus_proche_devant()) < 40)):
				if (self.peut_tirer()):
					return SoccerAction(self.prediction_ball(), self.vect_player_posi(self.adversaire_plus_proche_devant().x - self.cst_dribble_A, self.adversaire_plus_proche_devant().y + self.cst_dribble_B)/60)
				return self.courir_vers_ball_predi() 
			if (self.adversaire_devant_player() & self.au_dessu_nous(self.adversaire_plus_proche_devant()) & (self.dist_adversaire_player(self.adversaire_plus_proche_devant()) < 40)):
				if (self.peut_tirer()):
					return SoccerAction(self.prediction_ball(), self.vect_player_posi(self.adversaire_plus_proche_devant().x - self.cst_dribble_A, self.adversaire_plus_proche_devant().y - self.cst_dribble_B)/60)
				return self.courir_vers_ball_predi()
			return self.attaque_fonceur(id_team)
		if (self.adversaire_devant_player() & self.en_dessou_nous(self.adversaire_plus_proche_devant()) & (self.dist_adversaire_player(self.adversaire_plus_proche_devant()) < 40)):
			if (self.peut_tirer()):
				return SoccerAction(self.prediction_ball(), self.vect_player_posi(self.adversaire_plus_proche_devant().x + self.cst_dribble_A, self.adversaire_plus_proche_devant().y + self.cst_dribble_B)/60)
			return self.courir_vers_ball_predi()

		if (self.adversaire_devant_player() & self.au_dessu_nous(self.adversaire_plus_proche_devant()) & (self.dist_adversaire_player(self.adversaire_plus_proche_devant()) < 40)):
			if (self.peut_tirer()):
				return SoccerAction(self.prediction_ball(), self.vect_player_posi(self.adversaire_plus_proche_devant().x + self.cst_dribble_A, self.adversaire_plus_proche_devant().y - self.cst_dribble_B)/60)
			return self.courir_vers_ball_predi()
		return self.attaque_fonceur(id_team)












