import numpy as np
import matplotlib.pyplot as plt

from gatspy.periodic import LombScargle
from gatspy.periodic.template_modeler import RRLyraeTemplateModeler
from gatspy.datasets import fetch_rrlyrae

rrlyrae = fetch_rrlyrae()
t, y, dy, filts = rrlyrae.get_lightcurve(rrlyrae.ids[0])

mask = (filts == 'g')
t = t[mask]
y = y[mask]
dy = dy[mask]

period = rrlyrae.get_metadata(rrlyrae.ids[0])['P']

model = RRLyraeTemplateModeler('g')
#model = LombScargle()

model.fit(t, y, dy)

# Plot a best fit
tfit = np.linspace(0, period, 1000, endpoint=False)
yfit = model.predict(tfit, period)
plt.errorbar(t % period, y, dy, fmt='.')
plt.plot(tfit % period, yfit)

# Plot a score
periods = np.linspace(period - 1E-4, period + 1E-4, 10)
plt.figure()
plt.plot(periods, model.score(periods))
plt.ylim(0, 1)

plt.show()
