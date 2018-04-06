# coding: utf-8
from __future__ import print_function, division
from soccersimulator import SoccerTeam, Simulation, Strategy, show_simu, Vector2D
from soccersimulator.settings import GAME_WIDTH, GAME_HEIGHT
from Foot.strategies import Fonceur
import pickle

class SimpleParamSearch(object):
	def __init__(self, trials=10, max_round_step=100, discret=3):
		"""
		:param trials: nombre d'essais par endroit et par puissance
		:param max_round_step: durée maximale d'un essai
		:param discret: pas (step) de découpage du terrain.
			Attention, le nombre d'endroits testés est égal à discret^2
		"""
		self.trials = trials
		self.max_round_step = max_round_step
		self.list_forces = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5] #7
		self.list_grille = []
		#Fabrication de la grille de discretisation du terrain
		if discret == 1:
			self.stepx = 0
			self.stepy = 0
		else:
			self.stepx = GAME_WIDTH/(2.*discret)
			self.stepy = GAME_HEIGHT/(2.*discret -2)
			#D'où le if ==1
		for i in range(discret):
			for j in range(discret):
				self.list_grille.append(Vector2D(GAME_WIDTH/2. + self.stepx*i,
												self.stepy*j))
		self.strategy = Fonceur()
    
	def start(self, show=True):
		team1 = SoccerTeam("Team 1")
		team1.add("Test", self.strategy)
		self.simu = Simulation(team1, max_steps=100000)
		self.simu.listeners += self
		if show:
			show_simu(self.simu)
		else:
			self.simu.start()

	def begin_match(self, team1, team2, state):
		self.last = 0  # Step of the last round
		self.crit = 0  # Criterion to maximize (here, number of goals)
		self.cpt = 0  # Counter for trials
		self.res = dict()  # Dictionary of results
		self.idx_force = 0 # counter for parameter index
		self.idx_grille = 0
        
	def begin_round(self, team1, team2, state):
		# On fixe la position de la balle et du joueur
		ball_pos = self.list_grille[self.idx_grille]
		self.simu.state.states[(1, 0)].position = ball_pos.copy()  
		self.simu.state.states[(1, 0)].vitesse = Vector2D() 
		self.simu.state.ball.position = ball_pos.copy() 
		
		# Set the current value for the current parameter
		self.strategy.strength = self.list_forces[self.idx_force]

		# Last step of the game
		self.last = self.simu.step

	def update_round(self, team1, team2, state):
		# Stop the round if it is too long
		if state.step > self.last + self.max_round_step:
		    self.simu.end_round()

	def end_round(self, team1, team2, state):
		# A round ends when there is a goal
		if state.goal > 0:
			self.crit += 1 # Increment criterion
		self.cpt += 1  # Increment number of trials
		
		if self.cpt >= self.trials:
			key = (self.list_grille[self.idx_grille].x,
					self.list_grille[self.idx_grille].y)
			
			if key not in self.res:
				self.res[key]=[]
			self.res[key].append((self.list_forces[self.idx_force], self.crit*1./self.trials))
			print("Res pour position", key, "force", self.res[key][-1][0], ":", self.res[key][-1][1])
			# Reset parameters
			self.crit = 0
			self.cpt = 0
			# Go to the next parameter value to try
			self.idx_force += 1
			if self.idx_force >= len(self.list_forces):
				self.idx_grille += 1
				self.idx_force = 0
			if self.idx_grille>=len(self.list_grille):
				self.simu.end_match()

	def end_match(self, team1, team2, state):
		#Trouve les meilleurs paramètres et les sauvegarde
		meilleure_force = dict()
		for k,v in self.res.items():
			meilleure_force[k] = sorted(v, key=lambda x : x[1])[-1][0]
		with open("meilleure_force.pkl", "wb") as f:
			pickle.dump(meilleure_force, f)

if __name__=="__main__":
	psearch = SimpleParamSearch()
	psearch.start(False)
