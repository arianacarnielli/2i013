# -*- coding: utf-8 -*-
from soccersimulator import Vector2D, settings
from .etat import Etat
from .utilitaires import estDansTerrain, estSortant

#####################################################
#TIRS : Vector2D
#####################################################

def tir_but(etat):
	"""
	Tire vers le milieu des buts adverses.
	Plus fort si on est plus loin des cages.
	"""
	if etat.distance() <= etat.rayon_shoot:
		return etat.but_adv - etat.p_joueur
	else:
		return Vector2D()

def degage(etat):
	"""
	Tire le plus fort possible en direction des buts adverses.
	"""
	return (tir_but(etat)).scale(settings.maxPlayerShoot)
	#normalize() n'est pas suffisant, maxPlayerShoot est à 6.


#####################################################
#DEPLACEMENTS : Vector2D
#####################################################

def fonce(etat):
	"""
	Fonce vers la balle sans prédiction.
	Si on est à portée de shoot, ne bouge pas.
	"""
	if etat.distance() <= etat.rayon_shoot:
		return Vector2D()
	else:
		return (etat.p_balle - etat.p_joueur).normalize()
		#normalize() fixe à 1, qui est la vitesse maximale des joueurs

def defend(etat):
	"""	
	Si la balle est dans son camp, se dirige vers elle.
	Sinon, se place en défense (dans son camp) entre la balle et les buts.
	"""
	
	if estDansTerrain(etat, etat.p_balle) and not estSortant(etat, etat.ball):
		return fonce(etat)
	else:
		#Horizontal : Se replace vers le milieu de son terrain
		#Vertical : Se met entre le milieu de ses buts et la balle
		cible_x = etat.mon_terrain.x
		cible_y = (etat.mon_terrain.x - etat.mon_but.x)*(etat.p_balle.y - etat.mon_but.y)/(etat.p_balle.x - etat.mon_but.x) + etat.mon_but.y
		
		return Vector2D(cible_x - etat.p_joueur.x, cible_y - etat.p_joueur.y)





