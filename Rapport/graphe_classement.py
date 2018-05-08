# -*- coding: utf-8 -*-
"""
Created on Tue May  8 15:40:14 2018

@author: arian
"""

import matplotlib.pyplot as plt

sem1 = [4, 5, 6, 7, 8, 9, 10, 11]
sem2 = [   5, 6, 7, 8, 9, 10, 11]
sem4 = [                  10, 11]

class1 = [4, 4, 4, 7, 5, 6, 3, 1]
class2 = [   6, 1, 1, 1, 1, 1, 2]
class4 = [                  1, 1]

plt.close(1)
plt.figure(1, figsize=(5, 5))
plt.plot(sem1, class1, color=(0, 0.5, 1), lw=2, label="1v1")
plt.plot(sem2, class2, color=(0, 0.6, 0), lw=2, label="2v2")
plt.plot(sem4, class4, color=(1, 0.5, 0), lw=2, label="4v4")
plt.grid(True)
plt.gca().invert_yaxis()
plt.xlabel("Semaine")
plt.ylabel("Classement")
plt.legend(loc = "lower right")
