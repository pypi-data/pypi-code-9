
def deriv1(A0, B0, A1, B1, *args):
    """

        # The first derivative equation is (f(t+h) - f(t))/h

        was like this...
        view_diff = timeseries[0][1] - timeseries[1][1]
        time_diff = get_minute(timeseries[0][0] - timeseries[1][0])
        result[0] = view_diff / time_diff

    """

    Adiff = A0 - A1
    Bdiff = B0 - B1
    if Bdiff > 0:
        return Adiff / Bdiff
    return 0


def deriv2(A0, B0, A1, B1, A2, B2, *args):
    """
        # The second derivative equation is
        # (h2f(t+h1) + h1f(t-h2) - (h1+h2)f(t)) / ((h1+h2)h1h2/2)
        h1 = get_minute(timeseries[0][0] - timeseries[1][0])
        h2 = get_minute(timeseries[1][0] - timeseries[2][0])
        fh1 = timeseries[0][1]
        ft = timeseries[1][1]
        fh2 = timeseries[2][1]
        result[1] = h2 * fh1 + h1 * fh2 - (h1 + h2) * ft
        result[1] = result[1] / ((h1 + h2) * h1 * h2 / 2)

    """

    h1 = A0 - A1
    h2 = A1 - A2
    fh1 = B0
    ft = B1
    fh2 = B2
    result = h2 * fh1 + h1 * fh2 - (h1 + h2) * ft
    if any(a == 0 for a in [h1, h2]):
        return 0
    return result / ((h1 + h2) * h1 * h2 / 2)


funcs = [
    None,
    deriv1,
    deriv2
]


def calculate_derivatives(timeseries, attribute_pairs, depth=2):
    """
        attribute_pairs:
            [(view_count, time), (sub_count, time)]etc...

    """

    for A, B in attribute_pairs:
        args = []
        for t in timeseries[:max(2, len(timeseries))]:
            args.extend([getattr(t, A).to_json(), getattr(t, B).to_json()])
        results = []
        for order in range(1, depth+1):
            if len(args) >= 2 + 2*order:
                timeseries[0].set_derivatives(A, B, funcs[order](*args), order)
    return timeseries
