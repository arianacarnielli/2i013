from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import Simulation, SoccerTeam, Player, show_simu
from soccersimulator import Strategy
from soccersimulator import settings
from soccersimulator.settings import *
from .etat import *
import math

def dirballe(etat,norme) :
	vect = etat.posballe()-etat.posjoueur()
	vect.norm = norme
	return vect

def dirpos(etat,norme,pos):
	vect = pos-etat.posjoueur()
	vect.norm = norme
	return vect

def dirgoal(etat,norme) :
	vect=Vector2D(0,0)
	posg=etat.posgoal()
	vect=posg-etat.posballe()
	vect.norm=norme
	return vect

def deviation(etat,norme) :
	direction_goal=dirgoal(etat,norme)
	sp=etat.speed()
	balle=etat.posballe()
	if sp.x>0:
		anticipe=balle.y+(direction_goal.x/sp.x)*sp.y
		if anticipe>=GAME_HEIGHT/2-GAME_GOAL_HEIGHT and anticipe<=GAME_HEIGHT/2+GAME_GOAL_HEIGHT:
			if balle.y >=GAME_HEIGHT/2:
				direction_goal.angle += math.radians(25)
			if balle.y <GAME_HEIGHT/2:
				direction_goal.angle -= math.radians(25)
	return direction_goal

def dir_centre(etat) :
	return dirpos(etat,1,etat.posinter())

def dir_posdef(etat, prop) :
	return dirpos(etat,1,etat.posdef(prop))

def dir_pospasse(etat, id_player):
	return dirpos(etat,1,etat.pos_passe(id_player))

def passe(etat, id_player, norme):
	vitesse = etat.state.player_state(etat.id_team,id_player).vitesse
	vect = Vector2D(etat.poscoequipier(id_player).x - etat.posjoueur().x + 10*vitesse.x,etat.poscoequipier(id_player).y - etat.posjoueur().y +10*vitesse.y)
	vect.norm=norme
	return vect
