from soccersimulator import SoccerTeam, Simulation, show_simu,KeyboardStrategy,DTreeStrategy,load_jsonz,dump_jsonz
from soccersimulator import apprend_arbre, build_apprentissage, genere_dot
from modulesocc.strategies import *
from modulesocc.etat import Etat
import sklearn
import numpy as np
import pickle

assert sklearn.__version__ >= "0.18.1","Updater sklearn !! (pip install -U sklearn --user )"



### Transformation d'un etat en features : state,idt,idp -> R^d

def my_get_features(state,idt,idp):
	etat = Etat(state)
	f1 = etat.dist(etat.posjoueur(idt, idp), etat.posballe())
	f2 = etat.dist(etat.posgoal(idt))
	f3 = etat.dist(etat.posballe(), etat.posgoal(idt))
	return [f1,f2,f3]

my_get_features.names = ["dball","dbut","dballbut"]


def entrainer(fname):
    #Creation d'une partie
	kb_strat_def = KeyboardStrategy()
	kb_strat_def.add("a",posdefStrategy())
	kb_strat_def.add("z",passeStrategy())

	kb_strat_atk = KeyboardStrategy()
	kb_strat_atk.add("q",pospasseStrategy())
	kb_strat_atk.add("s",dribbleStrategy())
	kb_strat_atk.add("d",tirStrategy())
	
	team1 = SoccerTeam(name="Control Team")
	team2 = SoccerTeam(name="Sparing")
	team1.add("Defenseur",kb_strat_def)
	team1.add("Attaquant",kb_strat_atk)
	team2.add("Player1",AttaqueStrategy())
	team2.add("Player2",DefenseStrategy()) 
	simu = Simulation(team1,team2)
    #Jouer, afficher et controler la partie
	show_simu(simu)
	print("Nombre d'exemples : "+str(len(kb_strat_atk.states)))
	print("Nombre d'exemples : "+str(len(kb_strat_def.states)))
    # Sauvegarde des etats dans un fichier
	dump_jsonz(kb_strat_atk.states,fname)
	dump_jsonz(kb_strat_def.states,fname)

def apprendre(exemples, get_features,fname=None):
    #genere l'ensemble d'apprentissage
	data_train, data_labels = build_apprentissage(exemples,get_features)
    ## Apprentissage de l'arbre
	dt = apprend_arbre(data_train,data_labels,depth=10,feature_names=get_features.names)
    ##Sauvegarde de l'arbre
	if fname is not None:
		with open(fname,"wb") as f:
			pickle.dump(dt,f)
	return dt

if __name__=="__main__":

	entrainer("tree_test.pkl")

	dic_strategy = {FonceurStrategy().name:FonceurStrategy(),DefenseStrategy().name:DefenseStrategy()}

	states_tuple = load_jsonz("test_kb_strat.jz")
	apprendre(states_tuple,my_get_features,"tree_test.pkl")
	with open("tree_test.pkl","rb") as f:
		dt = pickle.load(f)
    # Visualisation de l'arbre
	genere_dot(dt,"test_arbre.dot")
    #Utilisation de l'arbre : arbre de decision, dico strategy, fonction de transformation etat->variables
	treeStrat1 = DTreeStrategy(dt,dic_strategy,my_get_features)
	treeteam = SoccerTeam("Arbre Team")
	team2 = SoccerTeam(name="Sparing")
	treeteam.add("Joueur 1",treeStrat1)
	treeteam.add("Joueur 2",treeStrat1)
	team2.add("Joueur 1", AttaqueStrategy())
	team2.add("Joueur 2",DefenseStrategy())
	simu = Simulation(treeteam,team2)
	show_simu(simu)

