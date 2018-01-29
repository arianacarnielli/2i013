from soccersimulator import ChallengeFonceurButeur, SoccerTeam,show_simu
from strategy import FonceurFaible

team = SoccerTeam("RandomEquipe")
team.add("RandomJoueur",FonceurFaible())

challenge = ChallengeFonceurButeur(team,max_but=20)
show_simu(challenge)
print("temps moyen : ",challenge.stats_score, "\nliste des temps",challenge.resultats)