import module

expe = module.ParamSearch(strategy=module.ShootBallStratOpt(acc = 1.),
                   params={'n': range(21)},  max_round_step= 500, trials = 100)
expe.start(show = False)
print(expe.get_res())

