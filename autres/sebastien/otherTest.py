from soccersimulator import SoccerTeam, Simulation, show_simu, Strategy
from strategies import RandomStrat, FonceurplayerNV0


## Creation d'une equipe
fonceurs = SoccerTeam(name="TeamFonceur")
random = SoccerTeam(name="RandomStratTeam")
fonceurs.add("FonceurStrat", FonceurplayerNV0())
random.add("RandomStrat", RandomStrat())   #deplacement aléatoire

#Creation d'une partie
simu = Simulation(fonceurs,random)
#Jouer et afficher la partie
show_simu(simu)
