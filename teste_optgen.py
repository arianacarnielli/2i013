# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 19:07:16 2018

@author: 3525837
"""

import module


expe = module.ParamSearch_gen(strategy1 = module.Def2StratOpt, strategy2 = module.DribleStratOpt2, max_round_step= 200, trials = 10)
expe.start(show = True)
