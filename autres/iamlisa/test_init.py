from module.__init__ import *
from soccersimulator import Simulation, show_simu

nb_players = 1

pyteam = get_team(nb_players)
thon = get_team(nb_players)

simu = Simulation(pyteam,thon)
show_simu(simu)
