from soccersimulator import Strategy, SoccerAction, Vector2D
from soccersimulator import SoccerTeam, Simulation
from soccersimulator import show_simu


## Fonceur intelligent
class Fonceur_Intelligent(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Random")
    def compute_strategy(self,state,id_team,id_player):
    	if ((state.ball.position - state.player_state(id_team,id_player).position).norm < 50):
    		if ((state.ball.position - state.player_state(id_team,id_player).position).norm < PLAYER_RADIUS + BALL_RADIUS):
    			if (id_team == 1):
    				if((state.player_state(2,id_player).position - state.player_state(id_team,id_player).position).norm < 50):
    					return SoccerAction(Vector2D(-75,10),Vector2D(-75,10))
    				if (state.ball.position.x > 112):
    					return SoccerAction(state.ball.position - state.player_state(id_team,id_player).position ,(Vector2D(150,45) - state.ball.position)/8)
    				return SoccerAction(0,(Vector2D(150,45) - state.ball.position)/75)
    			if (id_team == 2):
    				if (state.ball.position.x < 37):
    					return SoccerAction(state.ball.position - state.player_state(id_team,id_player).position ,(Vector2D(0,45) - state.ball.position)/8)
    				return SoccerAction(0,(Vector2D(0,45) - state.ball.position)/75)
    		else:
    			return SoccerAction(state.ball.position - state.player_state(id_team,id_player).position ,0)
    	else:
    		return SoccerAction(0,0)
    		
    		
    		
