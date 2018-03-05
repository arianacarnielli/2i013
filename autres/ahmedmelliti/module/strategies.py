from soccersimulator  import Strategy, SoccerAction, Vector2D, SoccerState
from soccersimulator import SoccerTeam, Simulation, Player
from soccersimulator import show_simu
from soccersimulator.settings import *
from .tools import *
import math
## Strategie aleatoire
class RandomStrategy(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Random")
	def compute_strategy(self,state,id_team,id_player):
		return SoccerAction(Vector2D.create_random(-0.5,0.5),Vector2D.create_random(-0.5,0.5))


## Strategie Fonceur
class FonceurStrategy(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Fonceur")
	def compute_strategy(self,state,id_team,id_player):
		t = Tools(state,id_team,id_player)
		
		if t.canshoot():
			return SoccerAction(t.goto(t.ball_position)*100,0)
		return SoccerAction(0, 0.08*(t.cage_adv - t.p_position))

## Strategie DefenseZone 
class DZStrategy(Strategy):
	def __init__(self):
		Strategy.__init__(self,"DZ")
	def compute_strategy(self,state,id_team,id_player):
		t = Tools(state,id_team,id_player)
		#print(t.adv_le_plus_proche())
		#if t.dbp()<1.65:
		a=Vector2D(GAME_WIDTH*3/4.,GAME_HEIGHT*3/4.)
		b=Vector2D(GAME_WIDTH*1/4.,GAME_HEIGHT*3/4.)
		print(t.p_position)
		#if not t.canshoot() and i==0:
			#0.8
		#    if (t.p_position.x-t.adv_le_plus_proche().x<150):
		#        return SoccerAction(0, 400*(t.cage_adv - t.p_position))
		#    return SoccerAction(0, 0.001*(t.cage_adv - t.p_position))		
		#if t.dbp()<=GAME_WIDTH/4.:
		#    return SoccerAction(t.goto(t.ball_position)*1,0)	
		#if  t.p_position.distance(a)<=10 :
		#    return SoccerAction(0,b)
		#    i=1
		#if  t.p_position.distance(b)<=10 :
		#    return SoccerAction(0, 0.08*(t.cage_adv - t.p_position))
		#    i=2
		#if t.dbp()<=GAME_WIDTH/4.:
		#    return SoccerAction(t.goto(t.ball_position)*1,0)
		#if t.p_position.distance(t.cage_adv)<GAME_WIDTH/4.:
		#    return SoccerAction(t.goto(Vector2D(GAME_WIDTH*3/4.,GAME_HEIGHT/2.)),0)
		if t.dbp()<= GAME_WIDTH/8 :
			return SoccerAction(t.goto(t.ball_position)*1,0)
		if t.dbp()== 0 :
			return SoccerAction(t.goto(t.ball_position)*1,0.08*(t.cage_adv - t.p_position))
		

		if t.canshoot():
			return SoccerAction(t.goto(t.ball_position)*1,0)
		#    print(t.p_position)
		#    print(t.p_position.distance(a))
		#    print(t.p_position.distance(b))
		#    if t.p_position.distance(a)<=5:
		#        return SoccerAction(0,t.shoot(b))
		#        print(t.p_position.distance(a))
		#        print(t.p_position.distance(a))
		#    if t.p_position.distance(b)<=10:
		#        return SoccerAction(0, 0.08*(t.cage_adv - t.p_position))
		#if not t.canshoot() : 
		#    print("In can shoot")
		#    return SoccerAction(0,t.shoot(a))   
		#else:
		#    print("In can't shoot")
		return SoccerAction(0, 0.08*(t.cage_adv - t.p_position))       
## Strategie FonceurA
class FonceurAStrategy(Strategy):
	def __init__(self):
		Strategy.__init__(self,"FonceurA")
	def compute_strategy(self,state,id_team,id_player):
		t = Tools(state,id_team,id_player)		
		if t.canshoot():
			return SoccerAction(t.goto(t.ball_position)*100,0)
		return SoccerAction(0, 0.01*(t.cage_adv - t.p_position))


class FonceurTestStrategy(Strategy):
	def __init__(self, strength=None):
		Strategy.__init__(self,"Fonceur")
		self.strength = strength
	def compute_strategy(self,state,id_team,id_player):
		C = ComportementNaif(SuperState(state,id_team,id_player))
		if self.strength:
			C.SHOOT_COEF = self.strength
			I = ConditionAttaque(C)
		return fonceur(I)


## Strategie New
class NewStrategy(Strategy):
	def __init__(self):
		Strategy.__init__(self,"New")
	def compute_strategy(self,state,id_team,id_player):
		t = Tools(state,id_team,id_player)
		a=Vector2D(GAME_WIDTH*3/4.,GAME_HEIGHT*3/4.)
		b=Vector2D(GAME_WIDTH*1/4.,GAME_HEIGHT*3/4.)
		print(t.ball_vitesse)
		if t.canshoot():
			if t.adv_le_plus_proche().distance(t.ball_position)>t.p_position.distance(t.ball_position) :
				if t.p_position.distance(t.cage_adv - t.p_position)<10:
					return SoccerAction(0, 0.1*(b - t.p_position))  
				else :
					print(t.adv_le_plus_proche())
					return SoccerAction(t.goto(t.ball_position)*1,0.1*(b - t.p_position))
			#if t.dbp()== 0 :
			#    return SoccerAction(t.goto(a), 0.1*(b - t.p_position))
							   
			#return SoccerAction(t.goto(t.ball_position)*100,0)
		if t.p_position.distance(b)<20:
			return SoccerAction(t.goto(t.ball_position)*1, 0)
		if t.p_position.distance(t.cage_adv - t.p_position)<50: 
			return SoccerAction(0, 0.1*(b - t.p_position))                     
		return SoccerAction(t.goto(a)*100, 0.1*(a - t.p_position))
		

class Fonceur(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Fonceur")
	def compute_strategy(self,state,id_team,id_player):
		t = Tools(state,id_team,id_player)
		if (t.canshoot1()):
			return t.shoot_cage()
		return SoccerAction(t.goto(t.ball_position))

class Fonceur_dribbleur(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Fonceur_dribbleur")
	def compute_strategy(self,state,id_team,id_player):
		t = Tools(state,id_team,id_player)
		print(t.canshoot1())
		if t.canshoot1():
				if t.joueur_position_shoot():
					return t.shoot_cage()
				else:
					return t.dribble()
		else:
			return SoccerAction(t.goto(t.ball_position+4*t.ball_vitesse))


class Milieu(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Milieu")
	def compute_strategy(self,state,id_team,id_player):
		t = Tools(state,id_team,id_player)
		print(t.ami_position)	
		if t.canshoot1():
			if t.joueur_position_shoot():
				return t.shoot_cage()
			return t.passe()
		elif t.au_milieu() or t.ball_avant_adv():
			return SoccerAction(t.goto(t.ball_position+4*t.ball_vitesse))
		else:
			return SoccerAction(t.goto(t.cage))

class Defenseur(Strategy):
	def __init__(self):
		Strategy.__init__(self,"Defenseur")
	def compute_strategy(self,state,id_team,id_player):
		t = Tools(state,id_team,id_player)
		if t.canshoot1():
			if t.joueur_position_shoot():
				return t.shoot_cage()
			else:
				return t.dribble()
		elif t.en_attaque() or t.ball_avant_adv_avc():
			return SoccerAction(t.goto(t.ball_position + t.ball_vitesse))
		else:
			return SoccerAction(t.goto(t.cage_adv))

