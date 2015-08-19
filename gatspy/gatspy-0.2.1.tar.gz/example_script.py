from time import time
import numpy as np

from gatspy import datasets, periodic

# Choose a Sesar 2010 object
lcid = 1019544
rrlyrae = datasets.fetch_rrlyrae()
t, mag, dmag, filts = rrlyrae.get_lightcurve(lcid)

# Instantiate the model

# Try a fast model
t0 = time()
model = periodic.LombScargleMultibandFast()
model.optimizer.period_range = (0.2, 1.2)
model.fit(t, mag, dmag, filts)
periods, scores = model.find_best_periods(5, return_scores=True)
print("{0:.2f} sec".format(time() - t0))

print(periods)
print(scores)

# Full model
t0 = time()
model = periodic.LombScargleMultiband()
model.optimizer.period_range = (0.2, 1.2)
model.fit(t, mag, dmag, filts)
periods, scores = model.find_best_periods(5, return_scores=True)
print("{0:.2f} sec".format(time() - t0))

print(periods)
print(scores)
