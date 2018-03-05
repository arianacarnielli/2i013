from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import Simulation, SoccerTeam, Player, show_simu
from soccersimulator import Strategy
from soccersimulator import settings
from soccersimulator.settings import *
import math

class Etat(object):
	def __init__(self,state,id_team,id_player):
		self.state = state
		self.id_team = id_team
		self.id_player = id_player
	
	def posballe(self) : #retourne la pos de la balle
		return self.state.ball.position
	
	def posjoueur(self) : #retourne la pos du joueur
		return self.state.player_state(self.id_team,self.id_player).position
	
	def speed(self) : #retourne la vitesse de la balle
		return self.state.ball.vitesse

	def posgoal(self) : #retourne la position des cages adverses
		if self.id_team==1:
			pos=Vector2D(GAME_WIDTH,GAME_HEIGHT/2)
		if self.id_team==2:
			pos=Vector2D(0,GAME_HEIGHT/2)
		return pos

	def distballe(self):
		posb=self.posballe()
		posj=self.posjoueur()
		return math.hypot(posb.x-posj.x,posb.y-posj.y)

	def can_shoot(self) : #retourne le booléen indiquant si le joueur peut tirer
		return (self.distballe() <= PLAYER_RADIUS+BALL_RADIUS)

	def posinter(self) : #retourne la position pour intercepter la balle au début du round
		posb=self.posballe()
		if self.id_team==1:
			posb.x-=2
		if self.id_team==2:
			posb.x+=2
		return posb

	def prox_adv(self): #retourne le numéro du joueur adverse le plus proche de la balle
		nb_adv=self.state.nb_players(self.id_team%2+1)
		dist_adv=GAME_WIDTH
		c=0
		nb_j=0
		while c<nb_adv :
			posj=self.state.player_state(self.id_team%2+1,c).position
			posb=self.posballe()
			dist=math.hypot(posb.x-posj.x,posb.y-posj.y)
			if dist<dist_adv:
				dist_adv=dist
				nb_j=c
			c+=1
		return nb_j

	def pos_passe(self, id_player1):
		posjd=self.state.player_state(self.id_team, id_player1).position
		posjadv=self.state.player_state(self.id_team%2+1, self.prox_adv()).position
		if (posjadv.y>=posjd.x):
			angle=-60
		else :
			angle=60
		vect=Vector2D(posjadv.x-posjd.x,posjadv.y-posjd.y)
		vect.angle += math.radians(angle)
		return Vector2D(posjd.x+vect.x,posjd.y+vect.y)
		
		
	def poscoequipier(self, id_player2):
		return self.state.player_state(self.id_team, id_player2).position

	def estcentre(self) : #retourne le boléen indiquant si la balle est centrée
		posb=self.posballe()
		return (posb.x==GAME_WIDTH/2 and posb.y==GAME_HEIGHT/2)

	def posdef(self,prop) : #retourne la position entre la balle et les cages avec la proportion donnée
		posb=self.posballe()
		if self.id_team==2:
			posg=Vector2D(GAME_WIDTH,GAME_HEIGHT/2)
		if self.id_team==1:
			posg=Vector2D(0,GAME_HEIGHT/2)
		return Vector2D((posb.x*(1-prop)+posg.x*prop),(posb.y*(1-prop)+posg.y*prop))

	def adv_balle(self) : #retourne le boléen indiquant si l'adversaire est plus proche de la balle
		posb=self.posballe()
		posj2=self.state.player_state(self.id_team%2+1,self.prox_adv()).position
		distj1=self.distballe()
		distj2=math.hypot(posb.x-posj2.x,posb.y-posj2.y)
		if distj1>=distj2 :
			return True
		else :
			return False

	def balle_def(self,ecart) : #retourne le boléen indiquant si la balle est dans la moitiée du terrain
		posb=self.posballe()
		if self.id_team==1 and posb.x - ecart<= GAME_WIDTH/2 :
			return True
		elif self.id_team==2 and posb.x + ecart >= GAME_WIDTH/2 :
			return True
		else :
			return False
