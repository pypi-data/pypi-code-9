def triangular(x, a, b, c):
    if x < a:
        return 0
    elif x < b:
        return (x-a) / (b-a)
    elif x < c:
        return (c-x) / (c-b)
    else:
        return 0
        
def trapezoidal(x, a, b, c, d):
    if x < a:
        return 0
    elif x < b:
        return (x-a) / (b-a)
    elif x < c:
        return 1
    elif x < d:
        return (d-x) / (d-c)
    else:
        return 0
