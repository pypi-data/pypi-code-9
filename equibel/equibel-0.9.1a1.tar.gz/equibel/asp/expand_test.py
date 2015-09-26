import gringo

def on_model(m):
    print(m)

def go():
    prg = gringo.Control()
    prg.load('expanding.lp')
    prg.load('expanding_cardinality.lp')
    prg.load('exami.lp')
    prg.ground([("base", [])])
    prg.ground([("expand", [1])])
    prg.solve(on_model=on_model)
    
    print("-------------------------------")

    prg = gringo.Control()
    prg.load('expanding.lp')
    prg.load('expanding_cardinality.lp')
    prg.load('simp.lp')
    prg.ground([("base", [])])
    prg.ground([("expand", [2])])
    prg.solve(on_model=on_model)


if __name__ == '__main__':
    go()
