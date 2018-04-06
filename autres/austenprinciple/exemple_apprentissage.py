from soccersimulator import SoccerTeam, Simulation, show_simu, KeyboardStrategy, DTreeStrategy, load_jsonz, dump_jsonz
from soccersimulator import apprend_arbre, build_apprentissage, genere_dot
from Foot.strategies import Fonceur, Defenseur
from Foot.etat import Etat

import sklearn
import numpy as np
import pickle

assert sklearn.__version__ >= "0.18.1","Updater sklearn !! (pip install -U sklearn --user )"


def extraction_attributs(state, id_t, id_p):
	"""
	Extraction d'attributs d'un état.
	Ici distance à la balle, distance au but, distance balle-but
	"""
	etat = Etat(state, id_t, id_p)
	
	attr1 = etat.distance()              	#Distance moi-balle
	attr2 = etat.distance(B=etat.mon_but)	#Distance moi-but
	attr3 = etat.distance(A=etat.mon_but)	#Distance but-balle
	
	return [attr1, attr2, attr3]

extraction_attributs.names = ["dist_balle","dist_but","dist_ball-but"]


def entrainer(fichier):
	"""
	Simule un match dans lequel on doit intervenir pour générer un fichier d'apprentissage.
	Contrôles : a pour Fonceur, d pour Défenseur.
	"""
	#Création des équipes
	kb_strat = KeyboardStrategy()
	kb_strat.add("a", Fonceur())
	kb_strat.add("d", Defenseur())

	team1 = SoccerTeam(name="Moi")
	team2 = SoccerTeam(name="Idiots")
	team1.add("ControlPlayer", kb_strat)
	team2.add("Player", Fonceur())

	#Jouer, afficher et controler la partie    
	simu = Simulation(team1, team2)
	show_simu(simu)

	print("Nombre d'exemples : " + str(len(kb_strat.states)))
	# Sauvegarde des états dans un fichier
	dump_jsonz(kb_strat.states, fichier)

def apprendre(exemples, fonc_attributs=extraction_attributs, fichier=None):
	"""
	Génère, à partir d'une liste d'exemples d'actions, un arbre d'apprentissage.
	Cet arbre est renvoyé et stocké dans le fichier <fichier> si besoin.
	"""
	#Génère l'arbre d'apprentissage
	data_train, data_labels = build_apprentissage(exemples, fonc_attributs)

	#Apprentissage de l'arbre
	dt = apprend_arbre(data_train, data_labels, depth=10, feature_names=fonc_attributs.names)

	#Sauvegarde de l'arbre
	if fichier is not None:
		with open(fichier, "wb") as f:
			pickle.dump(dt, f)
	return dt


if __name__=="__main__":

	entrainer("test_kb_strat.jz")

	dic_strategy = {Fonceur().name: Fonceur(), Defenseur().name: Defenseur()}

	states_tuple = load_jsonz("test_kb_strat.jz")
	apprendre(states_tuple, fichier="tree_test.pkl")
	with open("tree_test.pkl","rb") as f:
		dt = pickle.load(f)

	# Visualisation de l'arbre
	genere_dot(dt, "test_arbre.dot")
	
	#Utilisation de l'arbre : arbre de decision, dico strategy, fonction de transformation etat -> attributs
	treeStrat1 = DTreeStrategy(dt, dic_strategy, extraction_attributs)
	
	#Création des équipes
	treeteam = SoccerTeam(name="Arbre")
	team2 = SoccerTeam(name="Sparring")
	treeteam.add("Arbre 1", treeStrat1)
	treeteam.add("Arbre 2", treeStrat1)
	team2.add("Joueur 1", Fonceur())
	team2.add("Joueur 2", Defenseur())
	simu = Simulation(treeteam,team2)
	show_simu(simu)


