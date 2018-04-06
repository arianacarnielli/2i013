from soccersimulator import SoccerTeam, Simulation, show_simu, Strategy
from Foot.strategies import RandomStrategy, Fonceur, Defenseur

# Création des équipes
team_dig = SoccerTeam(name="Dignitas")
team_fnc = SoccerTeam(name="Fnatic")

team_dig.add("JayPL", Defenseur())
team_dig.add("Snitch", Fonceur())

team_fnc.add("Breez", Fonceur())
team_fnc.add("Mene", Fonceur())

# Création d'une partie
simu = Simulation(team_dig, team_fnc)

# Jouer et afficher la partie
show_simu(simu)
