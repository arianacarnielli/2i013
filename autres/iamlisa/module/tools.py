from soccersimulator  import Strategy, SoccerAction, Vector2D, SoccerState
from soccersimulator.settings import *
from math import exp

class Tools(object):
	def __init__(self,state,id_team,id_player):
		self.state = state
		self.id_team = id_team
		self.id_player = id_player

	#Position
	def ball(self):
		return self.state.ball.position

	def player(self):
		return self.state.player_state(self.id_team,self.id_player).position

	def player2(self,id_team,id_player):
		return self.state.player_state(id_team,id_player).position

	def his_team(self):
        	return (2 - self.id_team)+1

	def my_goal(self):
		if self.id_team==1:
			return Vector2D(0,GAME_HEIGHT/2.)
		else:
			return Vector2D(GAME_WIDTH, GAME_HEIGHT/2.)

	def his_goal(self):
		if self.id_team==1:
			return Vector2D(GAME_WIDTH, GAME_HEIGHT/2.)
		else:
			return Vector2D(0,GAME_HEIGHT/2.)


	#Vecteur
	def ball_goal(self):
		return self.his_goal()-self.ball()

	def player_ball(self):
		return self.ball()-self.player()

	def player_his_goal(self):
		return self.his_goal()-self.player()

	def player_my_goal(self):
		return self.my_goal()-self.player()

	def player_friend(self):
		return self.closest_friend()-self.player()

	def player_ennemi(self):
		return self.closest_ennemi()-self.player()


	#Distance
	def d_goal_player(self):
		return self.player().distance(self.his_goal())

	def d_ball_player(self):
		return self.player().distance(self.ball())


	#Fonction
	def f(self,alpha,dist):
		return 1/(1+exp(-alpha*(dist-30)))

	def g(self,alpha,dist):
		return 1-exp(-alpha*dist)


	#Condition
	def test_shoot(self):
		return self.ball().distance(self.player())<(PLAYER_RADIUS+BALL_RADIUS)

	def in_my_half(self):
		if self.id_team==1:
			return self.ball().x < (GAME_WIDTH/2.)
		else:
			return self.ball().x > (GAME_WIDTH/2.)

	def in_his_half(self):
		if self.id_team==1:
			return self.ball().x > (GAME_WIDTH/2.)
		else:
			return self.ball().x < (GAME_WIDTH/2.)

	def ennemi_in_my_perimeter(self):
		L=[(it, ip) for (it, ip) in self.state.players if it != self.id_team]
		u = False
		p = 30.
		for i in range(len(L)):
			if self.id_team==1:
				if self.player2(L[i][0],L[i][1]).x > self.player().x and self.player2(L[i][0],L[i][1]).x < self.player().x+p and self.player2(L[i][0],L[i][1]).y > self.player().y-p and self.player2(L[i][0],L[i][1]).y < self.player().y+p:
					u = True
			else:
				if self.player2(L[i][0],L[i][1]).x > self.player().x-p and self.player2(L[i][0],L[i][1]).x < self.player().x and self.player2(L[i][0],L[i][1]).y > self.player().y-p and self.player2(L[i][0],L[i][1]).y < self.player().y+p:
					u = True
		return u

	def ennemi_in_my_big_perimeter(self):
		L=[(it, ip) for (it, ip) in self.state.players if it != self.id_team]
		u = False
		p = 40.
		for i in range(len(L)):
			if self.id_team==1:
				if self.player2(L[i][0],L[i][1]).x > self.player().x and self.player2(L[i][0],L[i][1]).x < self.player().x+p and self.player2(L[i][0],L[i][1]).y > self.player().y-p and self.player2(L[i][0],L[i][1]).y < self.player().y+p:
					u = True
			else:
				if self.player2(L[i][0],L[i][1]).x > self.player().x-p and self.player2(L[i][0],L[i][1]).x < self.player().x and self.player2(L[i][0],L[i][1]).y > self.player().y-p and self.player2(L[i][0],L[i][1]).y < self.player().y+p:
					u = True
		return u

	def in_my_third(self):
		if self.id_team==1:
			return self.state.ball.position.x < (GAME_WIDTH/3.)
		else:
			return self.state.ball.position.x > ((2*GAME_WIDTH)/3.)

	def in_his_third(self):
		if self.id_team==1:
			return self.state.ball.position.x > ((2*GAME_WIDTH)/3.)
		else:
			return self.state.ball.position.x < (GAME_WIDTH/3.)

	def in_my_quarter(self):
		if self.id_team==1:
			return self.state.ball.position.x < (GAME_WIDTH/4.)
		else:
			return self.state.ball.position.x > ((3*GAME_WIDTH)/4.)

	def in_his_quarter(self):
		if self.id_team==1:
			return self.state.ball.position.x > ((3*GAME_WIDTH)/4.)
		else:
			return self.state.ball.position.x < (GAME_WIDTH/4.)

	def in_my_fifth(self):
		if self.id_team==1:
			return self.state.ball.position.x < (GAME_WIDTH/5.)
		else:
			return self.state.ball.position.x > ((4*GAME_WIDTH)/5.)

	def in_his_fifth(self):
		if self.id_team==1:
			return self.state.ball.position.x > ((4*GAME_WIDTH)/5.)
		else:
			return self.state.ball.position.x < (GAME_WIDTH/5.)

	def in_goal_perimeter(self):
		if self.id_team==1:
			return self.ball().x<(GAME_WIDTH)/5 and self.ball().y<(GAME_HEIGHT)*3/4 and self.ball().y>(GAME_HEIGHT)/4
		return self.ball().x>(GAME_WIDTH)*4/5 and self.ball().y<(GAME_HEIGHT)*3/4 and self.ball().y>(GAME_HEIGHT)/4

	def someone(self):
		return len([(it, ip) for (it, ip) in self.state.players if it == self.id_team])>1


	#Joueur
	def closest_friend(self):
		L = [(it, ip) for (it, ip) in self.state.players if ((it == self.id_team) & (ip != self.id_player))]
		s=0
		v=0
		if len(L)==1:
			return self.player2(self.id_team,L[0][1])
		for i in range(len(L)-1):
			if i==0:
				s= self.player().distance(self.player2(self.id_team,L[0][1]))
				v=L[0][1]
			u=self.player().distance(self.player2(self.id_team,L[i+1][1]))
			if s>u:
				s=u
				v=L[i+1][1]
		return self.player2(self.id_team,v)

	def closest_ennemi(self):
		L = [(it, ip) for (it, ip) in self.state.players if it != self.id_team]
		s=0
		v=0
		p=self.his_team()
		if len(L)==1:
			return self.player2(p,L[0][1])
		for i in range(len(L)-1):
			if i==0:
				s= self.player().distance(self.player2(p,L[0][1]))
				v=L[0][1]
			u=self.player().distance(self.player2(p,L[i+1][1]))
			if s>u:
				s=u
				v=L[i+1][1]
		return self.player2(p,v)


