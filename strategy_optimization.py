import module

expe = module.ParamSearch(strategy=module.DefStratOpt(),
                   params={'p': [0.5, 0.2, 1]},  max_round_step= 200)
expe.start()
print(expe.get_res())

