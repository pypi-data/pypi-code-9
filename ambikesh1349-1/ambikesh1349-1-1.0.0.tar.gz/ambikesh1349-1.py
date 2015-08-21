def test(x):
    for y in x:
        if isinstance(y,list):
            test(y)
        else:
            print(y)

