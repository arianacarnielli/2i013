from soccersimulator import ChallengeFonceurButeur, SoccerTeam,show_simu
from strategy import TesteStrategy

team = SoccerTeam("RandomEquipe")
team.add("RandomJoueur",TesteStrategy())

challenge = ChallengeFonceurButeur(team,max_but=20)
show_simu(challenge)
print("temps moyen : ",challenge.stats_score, "\nliste des temps",challenge.resultats)