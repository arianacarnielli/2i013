from soccersimulator import Vector2D, SoccerState, SoccerAction
from soccersimulator import Simulation, SoccerTeam, Player, show_simu
from soccersimulator import Strategy
from soccersimulator import settings
from soccersimulator.settings import *
from tools import *
from strats import *
import random
import math

## Strategie aleatoire
class RandomStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Random")
    def compute_strategy(self,state,id_team,id_player):
	idEnemy = idTEnemy(id_team)
        playerPositionX = state.player_state(id_team, id_player).position.x
	playerPositionY = state.player_state(id_team, id_player).position.y
	ballPositionX = state.ball.position.x
	ballPositionY = state.ball.position.y
	dist = math.hypot(ballPositionX - playerPositionX, ballPositionY - playerPositionY)
	if(dist < PLAYER_RADIUS + BALL_RADIUS and state.ball.position.x > GAME_WIDTH / 2):
        	return SoccerAction(Vector2D(angle=3.14,norm=0.2), vecteurShootGoal(state.ball, 0, state.player_state(id_team, id_player).position.y, 10))
	elif(dist < PLAYER_RADIUS + BALL_RADIUS):
        	return SoccerAction(Vector2D(angle=3.14,norm=0.2), vecteurShootGoal(state.ball, 0, GAME_HEIGHT / 2, 4.5))
	else:
		return SoccerAction(Vector2D(ballPositionX - playerPositionX,ballPositionY - playerPositionY).normalize() * maxPlayerAcceleration, Vector2D(0,0))



class RandomStrategy2(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Random")
    def compute_strategy(self,state,id_team,id_player):
	idEnemy = idTEnemy(id_team)
        playerPositionX = state.player_state(id_team, id_player).position.x
	playerPositionY = state.player_state(id_team, id_player).position.y
	ballPositionX = state.ball.position.x
	ballPositionY = state.ball.position.y
	dist = math.hypot(ballPositionX - playerPositionX, ballPositionY - playerPositionY)
	if (state.ball.position.x == (GAME_WIDTH / 2)) and (state.ball.position.y == (GAME_HEIGHT / 2)):
		return SoccerAction(Vector2D(0,0), Vector2D(0,0))
	elif(dist < PLAYER_RADIUS + BALL_RADIUS and state.ball.position.x > GAME_WIDTH / 2 and state.player_state(idEnemy, id_player).position.y > playerPositionY):
        	return SoccerAction(Vector2D(angle=3.14,norm=0.2), vecteurShootGoal(state.ball, 0, state.player_state(id_team, id_player).position.y, 10))
	elif(dist < PLAYER_RADIUS + BALL_RADIUS):
        	return SoccerAction(Vector2D(angle=3.14,norm=0.2), vecteurShootGoal(state.ball, 0, GAME_HEIGHT / 2, 10))
	else:
		return SoccerAction(Vector2D(ballPositionX - playerPositionX,ballPositionY - playerPositionY).normalize() * maxPlayerAcceleration, Vector2D(0,0))



class Strategy2(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Random")
    def compute_strategy(self,state,id_team,id_player):
        playerPositionX = state.player_state(id_team, id_player).position.x
	playerPositionY = state.player_state(id_team, id_player).position.y
	ballPositionX = state.ball.position.x
	ballPositionY = state.ball.position.y
	dist = math.hypot(ballPositionX - playerPositionX, ballPositionY - playerPositionY)
	if(dist < PLAYER_RADIUS + BALL_RADIUS):
        	return SoccerAction(Vector2D(angle=3.14,norm=0.2), vecteurShootGoal(state.ball, GAME_WIDTH, GAME_HEIGHT / 2, 10))
	else:
		return SoccerAction(Vector2D(ballPositionX - playerPositionX,ballPositionY - playerPositionY).normalize() * maxPlayerAcceleration, Vector2D(0,0))

## Creation d'une equipe
pyteam = SoccerTeam(name="Overwatch")
thon = SoccerTeam(name="Rainbow6")
pyteam.add("Lucio",RandomStrategy()) #Strategie qui ne fait rien
thon.add("Valkyrie",RandomStrategy2())   #Strategie aleatoire

#Creation d'une partie
simu = Simulation(pyteam,thon)
#Jouer et afficher la partie
show_simu(simu)
