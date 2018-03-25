from soccersimulator import ChallengeFonceurButeur, SoccerTeam,show_simu
from .modulesocc.strategies import *

team = SoccerTeam("Team")
team.add("RedOne",FonceurStrategy())

challenge = ChallengeFonceurButeur(team,max_but=20)
show_simu(challenge)
print("temps moyen : ",challenge.stats_score, "\nliste des temps",challenge.resultats)
