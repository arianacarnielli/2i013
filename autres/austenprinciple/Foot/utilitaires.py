# -*- coding: utf-8 -*-
from soccersimulator import settings, Ball
from .etat import Etat


def estDansTerrain(etat, objet, home=True):
	"""
	Calcule si l'objet donné est de ce côté du terrain ou non.
	:param etat: Etat
	:param objet: Vector2D de la position de l'objet que l'on veut tester
	:param home: bool : True pour chez moi, False pour l'adversaire
	:return: bool
	"""
	
	if (etat._id_team == 1 and home) or (etat._id_team == 2 and not home):
		#Terrain gauche
		return objet.x < settings.GAME_WIDTH/2
	else:
		#Terrain droit
		return objet.x > settings.GAME_WIDTH/2
	

def estSortant(etat, objet, home=True):
	"""
	Calcule si l'objet donné est en train de sortir de ce côté du terrain.
	:param etat: Etat
	:param objet: MobileMixin : objet que l'on veut tester
	:param home: bool : True pour chez moi, False pour l'adversaire
	:return: bool
	"""
	
	if not estDansTerrain(etat, objet.position, home):
		return False
	
	if (etat._id_team == 1 and home) or (etat._id_team == 2 and not home):
		#Terrain gauche
		return (objet.position.x + objet.vitesse.x) > settings.GAME_WIDTH/2
	else:
		#Terrain droit
		return (objet.position.x + objet.vitesse.x) < settings.GAME_WIDTH/2
	

def oracleBalle(balle, n):
	"""
	Calcule la position de la balle dans n etapes.
	:param balle: Ball
	:param n: int
	:return: Vector2D
	"""
	
	new_B = Ball(balle.position, balle.vitesse)
	for i in range(n):
		new_B.next
	
	return new_B.position
	
	
	
	

