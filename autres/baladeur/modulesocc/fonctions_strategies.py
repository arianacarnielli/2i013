from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import Simulation, SoccerTeam, Player, show_simu
from soccersimulator import Strategy
from soccersimulator import settings
from soccersimulator.settings import *
from .actions_simples import *
from .etat import *
import math
from random import *

#Fonce vers la balle, tire toujours à une force = shoot
def fonceur_defaut(state,id_t,id_p, shoot) :
	e=Etat(state)
	if e.can_shoot(id_t,id_p) :
		return SoccerAction(dirballe(e,id_t,id_p, 1, 0), dirgoal(e, id_t%2+1, shoot, (0.8-0.2)*random()+0.2))
	else :
		return SoccerAction(dirballe(e,id_t,id_p, 1, 10))

def dribble(state,id_t,id_p) :
	e=Etat(state)
	if e.can_shoot(id_t,id_p) :
		return SoccerAction(dirballe(e,id_t,id_p, 1, 0), dirgoal(e, id_t%2+1, 2, 0.5))
	else :
		return SoccerAction(dirballe(e,id_t,id_p, 1, 10))


#Reste en défense, fait la passe au joueur allié le plus proche
def defense(state,id_t,id_p, shoot):
	e=Etat(state)
	posb=e.posballe()
	posg=e.poscage(id_t)
	posj=e.posjoueur(id_t,id_p)
	#le défenseur ira vers la balle si il est le plus proche, si la balle est trop proche des cages
	#ou si la balle est très éloignée des cages
	if (not(e.adv_prox(id_t,id_p)) and e.dist(posg,posb)<GAME_WIDTH/2.05) :
		nb_j=e.proche_joueur(id_t,id_p)
		if e.can_shoot(id_t,id_p) and nb_j != id_p : #le défenseur passe la balle à un équipier
			return SoccerAction(dirballe(e,id_t,id_p, 1, 0), passedef(e,id_t,nb_j, shoot, 1))
		elif e.can_shoot(id_t,id_p) and nb_j== id_p : #le défenseur n'a pas de coéquipier
			return SoccerAction(dirballe(e,id_t,id_p, 1, 0), dirgoal(e,id_t%2+1, shoot, 0.5))
		else :
			return SoccerAction(dirballe(e,id_t,id_p, 1, 2))
	elif e.balle_def(id_t%2+1, 0.4) and e.dist(posj,posb)<=50 :
		return fonceur_defaut(state,id_t,id_p,shoot)
	else : 
		return SoccerAction(dirpos(e,id_t, id_p, 1, e.posdef(id_t,0.4)))

#Attaque, receptionne les passes du défenseur (s'il y en a)
def attaque(state, id_t,id_p, shoot) :
	e=Etat(state)
	id_jd=e.proche_joueur(id_t,id_p)
	id_jb=e.proche_balle(id_t)
	if id_jd != id_p and id_jb != id_p:
		vect = 	dirpos(e,id_t,id_p,1,e.pospasse(id_t, id_jd, 25))
		return SoccerAction(vect)
	else :
		if e.dist(e.posballe(),e.poscage(id_t%2+1))>=50 :
			return dribble(state,id_t,id_p)
		else :
			return fonceur_defaut(state, id_t, id_p, shoot)

#mini-strategie position de reception de passe
def recpasse(state, id_t, id_p):
	e=Etat(state)
	id_jd=e.proche_joueur(id_t,id_p)
	vect = 	dirpos(e,id_t,id_p,1,e.pospasse(id_t, id_jd, 25))
	return SoccerAction(vect)

#mini-strategie passe la balle
def fairepasse(state, id_t, id_p,shoot):
	e=Etat(state)
	nb_j=e.proche_joueur(id_t,id_p)
	if e.can_shoot(id_t,id_p):
		return SoccerAction(dirballe(e,id_t,id_p, 1, 0), passedef(e,id_t,nb_j, shoot, 1))
	else :
		return SoccerAction(dirballe(e,id_t,id_p, 1, 2))

#mini-strategie va en position defensive
def arriere(state, id_t, id_p):
	e=Etat(state)
	return SoccerAction(dirpos(e,id_t, id_p, 1, e.posdef(id_t,0.4)))
