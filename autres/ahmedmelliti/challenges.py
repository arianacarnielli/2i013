#from .settings import *
from soccersimulator  import Strategy, SoccerAction, Vector2D, SoccerState
from soccersimulator import SoccerTeam, Simulation, Player
from soccersimulator import show_simu, mdpsoccer, utils
#from .mdpsoccer import *
#from .utils import *
from soccersimulator.settings import *
from strategies  import *

class ChallengeFonceurButeur(Simulation):
    def __init__(self,team1,max_but=10,max_steps=5*settings.MAX_GAME_STEPS,initial_state=None,**kwargs):
        super(ChallengeFonceurButeur,self).__init__(team1,None,max_steps,initial_state,**kwargs)
        self.name = self.__class__.__name__
        self.resultats = []
        self._last_step = 0
        self.max_but = max_but
        self.stats_score = 0
    def begin_round(self):
        self._last_step = self.state.step
        super(ChallengeFonceurButeur,self).begin_round()
    def update_round(self):
        super(ChallengeFonceurButeur,self).update_round()
    def end_round(self):
        if self.state.goal==1:
            self.resultats.append(self.state.step-self._last_step)
        super(ChallengeFonceurButeur,self).end_round()
    def stop(self):
        return super(ChallengeFonceurButeur,self).stop() or self.state.get_score_team(1) >=self.max_but
    def end_match(self):
        if len(self.resultats)>0:
            self.stats_score = sum(self.resultats)/len(self.resultats)
