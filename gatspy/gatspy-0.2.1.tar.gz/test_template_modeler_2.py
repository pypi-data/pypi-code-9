import numpy as np
import matplotlib.pyplot as plt

from gatspy.periodic import LombScargle
from gatspy.periodic.template_modeler import RRLyraeTemplateModelerMultiband
from gatspy.datasets import fetch_rrlyrae

rrlyrae = fetch_rrlyrae()
t, y, dy, filts = rrlyrae.get_lightcurve(rrlyrae.ids[0])
period = rrlyrae.get_metadata(rrlyrae.ids[0])['P']

#mask = (filts == 'g') | (filts == 'r') | (filts == 'i')
#t = t[mask]
#y = y[mask]
#dy = dy[mask]
#filts = filts[mask]

model = RRLyraeTemplateModelerMultiband()

model.fit(t, y, dy, filts)

# Plot a best fit
tfit = np.linspace(0, period, 1000, endpoint=False)
filtsfit = np.array(list('ugriz'))[:, None]
yfit = model.predict(tfit, filtsfit, period=period)

for i, filt in enumerate('ugriz'):
    mask = (filts == filt)
    l = plt.plot(tfit % period, yfit[i])
    plt.errorbar(t[mask] % period, y[mask], dy[mask], fmt='.',
                 color=l[0].get_color(), ecolor='gray')

plt.ylim(plt.ylim()[::-1])
plt.title('Multiband template fit')

# Plot score as a function of period
periods = np.linspace(period - 1E-4, period + 1E-4, 10)
plt.figure()
plt.plot(periods, model.score(periods))
plt.ylim(0, 1)

plt.show()
