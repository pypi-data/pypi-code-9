"""This is the "pyso_integrate.py" module and it provides one function called integrate()
	which return the integrate value of any one variable function provided."""

def integrate(func, start, end):
	"""This function takes three positional arguments called func, start, end
	   which are function needed to be integrated, a start point to calculate,
	   and the end point to finish.
	   The return value is an area which is exactly integration value needed.
	   Return value may not be exactly accurate."""
    step = 0.00001
    intercept = start
    area = 0
    while intercept < end:
        intercept += step
        bric = 0.5*(func(intercept)*step + func(intercept-step)*step)
        area += bric
    return area
