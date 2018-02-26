import module

expe = module.ParamSearch(strategy=module.PassStratOpt(),
                   params={'tooClose': [50]},  max_round_step= 200, trials = 10)
expe.start(show = True)
print(expe.get_res())

#  params={'tooClose': range(100)},  max_round_step= 200, trials = 1)