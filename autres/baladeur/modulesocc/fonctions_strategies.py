from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import Simulation, SoccerTeam, Player, show_simu
from soccersimulator import Strategy
from soccersimulator import settings
from soccersimulator.settings import *
from .actions_simples import *
from .etat import *
import math

def zigzag(state,id_team,id_player) :
	e=Etat(state,id_team,id_player)
	if e.balle_def(0) and e.adv_balle() :
		return SoccerAction(dir_posdef(e,0.5))
	else :
		if e.can_shoot() :
			return SoccerAction(dirballe(e,1),deviation(e,4))
		else :
			return SoccerAction(dirballe(e,1))

def defense(state,id_team,id_player) :
	e=Etat(state,id_team,id_player)
	if not(e.adv_balle()) :
		if e.can_shoot() :
			return SoccerAction(dirballe(e,1),passe(e,1,3))
		else :
			return SoccerAction(dirballe(e,1))
		return SoccerAction(dir_posdef(e,0.5))
	else :
		return SoccerAction(dir_posdef(e,0.5))
		

def attaquant(state,id_team,id_player) :
	e=Etat(state,id_team,id_player)
	if e.balle_def(10) and e.adv_balle() :
		return SoccerAction(dir_pospasse(e,0))
	else :
		if e.can_shoot() :
			return SoccerAction(dirballe(e,1),deviation(e,4))
		else :
			return SoccerAction(dirballe(e,1))
