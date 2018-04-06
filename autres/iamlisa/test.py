from soccersimulator import SoccerTeam, Simulation, Player
from soccersimulator import show_simu
from module.strategy import *

# Creation d'une equipe
pyteam = SoccerTeam(name="PyTeam")
thon = SoccerTeam(name="ThonTeam")

pyteam.add("PyDefenseur",DefenseurStrategy())
pyteam.add("PyFonceur1",Fonceur1Strategy())
#pyteam.add("PyFonceur2",Fonceur2Strategy())
#pyteam.add("PyFonceur3",Fonceur3Strategy())

#thon.add("ThonFonceur1",Fonceur1Strategy())
#thon.add("ThonFonceur2",Fonceur2Strategy())
thon.add("ThonDefenseur",DefenseurStrategy())
thon.add("ThonFonceur3",Fonceur3Strategy())

#Creation d'une partie
simu = Simulation(pyteam,thon)
#Jouer et afficher la partie
show_simu(simu)


