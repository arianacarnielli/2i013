# -*- coding: utf-8 -*-
from soccersimulator import Vector2D, settings


class Etat():
	def __init__(self, state, id_team, id_player):
		self._state = state
		self._id_team = id_team
		self._id_player = id_player

	def __getattr__(self, attr):
		return getattr(self._state, attr)

	@property
	def p_joueur(self):
		"""
		Position du joueur : Vector2D
		"""
		return self._state.player_state(self._id_team, self._id_player).position
	
	@property
	def joueur(self):
		"""
		Joueur actuel : PlayerState
		"""
		return self._state.player_state(self._id_team, self._id_player)
	
	@property
	def p_balle(self):
		"""
		Position de la balle : Vector2D
		"""
		return self._state.ball.position
	
	@property
	def mon_but(self):
		"""
		Position du but du joueur : Vector2D
		"""
		return Vector2D((self._id_team - 1)*settings.GAME_WIDTH, settings.GAME_HEIGHT/2)

	@property
	def mon_terrain(self):
		"""
		Adresse horizontale du milieu du terrain du joueur : Vector2D
		"""
		return Vector2D((2*self._id_team-1)*settings.GAME_WIDTH/4, 0)

	@property
	def but_adv(self):
		"""
		Position du but adverse : Vector2D
		"""
		return Vector2D((2 - self._id_team)*settings.GAME_WIDTH, settings.GAME_HEIGHT/2)
		
	@property
	def terrain_adv(self):
		"""
		Adresse horizontale du milieu du terrain du joueur adverse : Vector2D
		"""
		return Vector2D(((-2)*self._id_team+5)*settings.GAME_WIDTH/4, 0)

	@property
	def rayon_shoot(self):
		"""
		Rayon d'un joueur + rayon de la balle.
		"""
		return settings.PLAYER_RADIUS + settings.BALL_RADIUS
	
	def distance(self, A=None, B=None):
		"""
		Distance entre deux objets (Vector2D), par défaut le joueur actuel et la balle.
		-> Vector2D
		"""
		if not A:
			A = self.p_joueur
		if not B:
			B = self.p_balle
			
		return A.distance(B)
	


