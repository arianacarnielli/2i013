# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 21:07:54 2018

@author: arian
"""

import numpy as np
import matplotlib.pyplot as plt


score_max = np.empty(11, dtype = int)

score_moy = np.empty(11)

divers_moy = np.empty(11)

for i in range(10):
    data = np.load("genetique_4_{}_20180407.npz".format(i))
    score_max[i] = data["arr_1"].max()
    
    score_moy[i] = np.mean(data["arr_1"])
    
    divers_temp = np.empty_like(data["arr_0"][0])
    
    for j in range(divers_temp.size):
        arr_temp = np.empty(data["arr_0"].size)
        
        for k in range(arr_temp.size):
            arr_temp[k] = data["arr_0"][k][j]
        
        divers_temp[j] = np.unique(arr_temp).size
        
    divers_moy[i] = np.mean(divers_temp)

i = 10 
data = np.load("genetique_4_final_20180407.npz")
score_max[i] = data["arr_1"].max()

score_moy[i] = np.mean(data["arr_1"])

divers_temp = np.empty_like(data["arr_0"][0])

for j in range(divers_temp.size):
    arr_temp = np.empty(data["arr_0"].size)
    
    for k in range(arr_temp.size):
        arr_temp[k] = data["arr_0"][k][j]
    
    divers_temp[j] = np.unique(arr_temp).size
    
divers_moy[i] = np.mean(divers_temp)

plt.close(1)
plt.figure(1, figsize = (5, 5))
plt.plot(score_moy, "b-", lw = 2)
plt.grid(True)
plt.title("Évolution du score moyen")
plt.xlabel("Génération")
plt.ylabel("Score moyen")

plt.close(2)
plt.figure(2, figsize = (5, 5))
plt.plot(divers_moy, "b-", lw = 2)
plt.grid(True)
plt.title("Évolution de la diversité moyenne")
plt.xlabel("Génération")
plt.ylabel("Diversité moyenne")

