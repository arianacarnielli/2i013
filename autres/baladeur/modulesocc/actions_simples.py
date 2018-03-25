from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import Simulation, SoccerTeam, Player, show_simu
from soccersimulator import Strategy
from soccersimulator import settings
from soccersimulator.settings import *
from .etat import *
import math

#Vecteur direction vers la balle avec k tours d'anticipation
def dirballe(etat, id_t, id_p, norme, k) :
	vect= etat.posballe()+k*etat.spballe() - etat.posjoueur(id_t,id_p)
	vect.norm = norme
	return vect

#Vecteur direction vers la position indiquée
def dirpos(etat, id_t, id_p, norme, pos) :
	vect= pos-etat.posjoueur(id_t,id_p)
	vect.norm = norme
	return vect

#Vecteur tir de la balle vers les cages de la team indiquée, avec h correpondant au y visé
#h=0 	:	Tir vers le point le plus bas des cages
#h=0.5	:	Tir vers le centre
#h=1 	:	Tir vers le point le plus haut des cages
def dirgoal(etat, id_t, norme, h) : 
	posg=etat.poscage(id_t)
	hg=(GAME_HEIGHT-GAME_GOAL_HEIGHT)/2
	posb=etat.posballe()
	vect=Vector2D(posg.x-posb.x,(hg+h*GAME_GOAL_HEIGHT)-posb.y)
	vect.norm=norme
	return vect
	

#Vecteur tir de la balle vers un joueur allié de l'équipe avec k tours d'anticipation
def passe(etat, id_t, id_p, norme, k) :
	posb=etat.posballe()
	posp=etat.posjoueur(id_t,id_p)
	vitp=etat.spjoueur(id_t,id_p)
	vect=Vector2D(posp.x-posb.x+k*vitp.x,posp.y-posb.y+k*vitp.y)
	vect.norm=norme
	return vect

#Vecteur tir de la balle vers un joueur allié décalé par rapport à la position défensive
#k est le facteur du vecteur qui sépare le joueur allié du joueur adverse
def passedef(etat, id_t, id_p, norme, k) :
	t_adv = id_t%2+1
	posjadv=etat.state.player_state(t_adv, etat.proche_balle(t_adv)).position
	posj=etat.state.player_state(id_t,id_p).position
	pos=Vector2D(posj.x + k*(posj.x-posjadv.x), posj.y + k*(posj.y-posjadv.y))
	vect= pos-etat.posballe()
	vect.norm = norme
	return vect
