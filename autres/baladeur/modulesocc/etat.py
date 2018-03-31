from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import Simulation, SoccerTeam, Player, show_simu
from soccersimulator import Strategy
from soccersimulator import settings
from soccersimulator.settings import *
import math

class Etat(object):
	def __init__(self,state) :
		self.state = state
	
	#Position de la balle
	def posballe(self) 	:
		return self.state.ball.position

	#Vitesse de la balle
	def spballe(self) 	:
		return self.state.ball.vitesse

	#Position d'un joueur
	def posjoueur(self,id_t,id_p) 	:
		return self.state.player_state(id_t,id_p).position

	#Vitesse d'un joueur
	def spjoueur(self,id_t,id_p)	:
		return self.state.player_state(id_t,id_p).vitesse

	#Booléen indiquant si la balle est au centre
	def est_centre(self) :	
		posb=self.posballe()
		return (posb.x==GAME_WIDTH/2 and posb.y==GAME_HEIGHT/2)

	#Position des cages de l'équipe
	def poscage(self,id_t)	:
		if id_t==2:
			pos=Vector2D(GAME_WIDTH,GAME_HEIGHT/2)
		if id_t==1:
			pos=Vector2D(0,GAME_HEIGHT/2)
		return pos

	#Distance entre deux positions
	def dist(self,pos1,pos2)	:
		return math.hypot(pos1.x-pos2.x,pos1.y-pos2.y)

	#Booléen indiquant si le joueur peut tirer
	def can_shoot(self, id_t, id_p)	:
		return(self.dist(self.posballe(),self.posjoueur(id_t,id_p)) <= PLAYER_RADIUS+BALL_RADIUS)

	#Numéro du joueur de l'équipe donnée le plus proche de la balle
	def proche_balle(self, id_t) :
		nb_j=self.state.nb_players(id_t)
		distmin=math.sqrt(GAME_WIDTH**2+GAME_HEIGHT**2)
		posb=self.posballe()
		c=0
		num_j=0
		while c<nb_j :
			posj=self.state.player_state(id_t,c).position
			distj=self.dist(posb,posj)
			if distj<distmin :
				distmin=distj
				num_j=c
			c+=1
		return num_j

	#Numéro du joueur allié le plus proche du joueur choisi
	def proche_joueur(self,id_t,id_p):
		nb_j=self.state.nb_players(id_t)
		distmin=math.sqrt(GAME_WIDTH**2+GAME_HEIGHT**2)
		posp=self.posjoueur(id_t,id_p)
		c=0
		num_j=id_p
		while c<nb_j :
			posj=self.state.player_state(id_t,c).position
			distj=self.dist(posp,posj)
			if distj < distmin and c != id_p:
				distmin=distj
				num_j=c
			c+=1
		return num_j

	#Position pour la reception de la passe
	def pospasse(self, id_t, id_jd, h) :
		t_adv=id_t%2+1
		posb=self.posballe()
		posjd=self.state.player_state(id_t, id_jd).position
		posjadv=self.state.player_state(t_adv, self.proche_balle(t_adv)).position
		spejadv=self.spjoueur(t_adv,self.proche_balle(t_adv))
		posjadv=posjadv+10*spejadv
		if posjadv.y>posjd.y:
			k=-1
		else:
			k=1
		if posjadv.y<20 or posjadv.y>GAME_HEIGHT-20 : #Vérifie si la balle est trop proche du bords
			k=k*-1
		return Vector2D(posjadv.x,posjadv.y+k*h)

	#Position entre la balle et les cages
	def posdef(self, id_t, prop) :
		spe=self.spballe()
		posb=self.posballe()
		posc=self.poscage(id_t)	
		distx=posc.x-posb.x #calcul de la distance en x séparant la balle des cages
		if spe.x/distx >= 0 and spe.x >0 :
			k=distx/spe.x 
			arriv=posb.y+k*spe.y #calcul du point d'arrivée en y de la balle dans les cages
			return Vector2D((posb.x*(1-prop)+posc.x*prop),(posb.y*(1-prop)+arriv*prop))
		else :
			return Vector2D((posb.x*(1-prop)+posc.x*prop),(posb.y*(1-prop)+posc.y*prop))

	#Booléen indiquant si un adversaire est plus proche de la balle que le joueur
	def adv_prox(self,id_t,id_p) :
		t_adv=id_t%2+1
		posb=self.posballe()
		posj=self.state.player_state(id_t,id_p).position
		posadv=self.state.player_state(t_adv,self.proche_balle(t_adv)).position
		distj=self.dist(posb,posj)
		distadv=self.dist(posb,posadv)
		if distadv<distj :
			return True
		else :
			return False

	#Booléen indiquant si la balle est dans la partie du terrain correspondant à la proportion
	#prop = 0.5 	: la balle est dans la moitiée du terrain des cages de l'équipe
	#prop = 0.25 	: la balle est dans le quart du terrain des cages de l'équipe
	def balle_def(self,id_t,prop) :
		posb=self.posballe()
		if id_t==1 and posb.x <= prop*GAME_WIDTH :
			return True
		elif id_t==2 and posb.x >= GAME_WIDTH - (prop*GAME_WIDTH) :
			return True
		else :
			return False
		
		
