def extend(module):
    """
    * f, g, h are often reserved for functions
    * i, j, k, l, m, n are often indices
    * t is the t distribution

    ... but everything else is nice to have defined out of the box
    """

    keys = 'a b c d e o p q r s u v w x y z'
    return dict(list(zip(keys.split(), module.symbols(keys))))