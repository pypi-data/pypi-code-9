import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from cStringIO import StringIO
import base64

class Row(object):
    name = None
    arm = None
    weight = None

    def __init__(self, name = None, arm = 0.0, weight = 0.0):
        super(Row, self).__init__()
        self.name = name if name else "unknown"
        self.arm = arm
        self.weight = weight

    @property
    def moment(self):
        return float(self.weight) * float(self.arm)

    def __getitem__(self, key):
        if key == 0:
            key = 'weight'
        elif key == 1:
            key = 'arm'
        elif key == 2:
            key = 'moment'
        elif key == 3:
            key = 'name'
        return getattr(self, key)

    def __setitem__(self, key, value):
        if key == 0:
            key = 'weight'
        elif key == 1:
            key = 'arm'
        elif key == 2:
            raise ValueError("You cannot set moment manually")
        elif key == 3:
            key = 'name'
        setattr(self, key, value)

class Envelope(object):
    name = None
    points = None

    def __init__(self, name):
        super(Envelope, self).__init__()
        self.points = []
        self.name = name
    
    def addPoint(self, moment, weight):
        self.points.append((moment, weight))
        
        
class WeightBalance(object):
    rows = None
    envelopes = None
    weightUnit = None
    mtow = None

    def __init__(self, weightUnit = 'kg', mtow=0):
        super(WeightBalance, self).__init__()
        self.rows = []
        self.envelopes = []
        self.weightUnit = weightUnit
        self.mtow = mtow

    def addEnvelope(self, envelope):
        self.envelopes.append(envelope)
        
    def addRow(self, arm, weight, name=None):
        self.rows.append(Row(arm=arm, weight=weight, name=name))

    def calculate(self):
        weight = 0
        moment = 0
        for r in self.rows:
            weight += r['weight']
            moment += r['moment']
        return (weight, moment/weight, moment, True if weight <= self.mtow else False)

    def plot(self):
        fig, ax = plt.subplots()

        # Draw current weight and Balance
        x = self.calculate()
        color = 'g' if x[3] else 'r'
        plt.scatter(x[1], x[0], marker="D", s=100, color=color)
        ax.text(x[1], x[0]-(x[0]/100.0*6.0), 'Weight %(w)d%(u)s (%(m)d%(u)s mtow)' % {'w':x[0], 'u':self.weightUnit, 'm':self.mtow}, color=color)

        # Draw envelopes
        for e in self.envelopes:
            path = mpath.Path(e.points)
            patch = mpatches.PathPatch(path, alpha=0.0)
            ax.add_patch(patch)
            x, y = zip(*path.vertices)
            ax.plot(x, y, 'o--', label="%s" % e.name)

        # global parameters for the plot result
        ax.legend()
        plt.xlabel("Arm")
        plt.ylabel("Weight (%s)" % self.weightUnit)
        ax.grid()

        sio = StringIO()
        plt.savefig(sio, format='png')
        sio.seek(0)

        return base64.b64encode(sio.getvalue())


if __name__ == "__main__":
    envelope = Envelope('Normal')
    envelope.addPoint(moment=1.841, weight=350)
    envelope.addPoint(moment=1.841, weight=630)
    envelope.addPoint(moment=1.978, weight=630)
    envelope.addPoint(moment=1.978, weight=350)

    #envelope2 = Envelope('Utility')
    #envelope2.addPoint(moment=1.811, weight=350)
    #envelope2.addPoint(moment=1.811, weight=830)
    #envelope2.addPoint(moment=1.918, weight=830)
    #envelope2.addPoint(moment=1.918, weight=350)

    wb = WeightBalance(mtow=630)
    wb.addEnvelope(envelope)
    #wb.addEnvelope(envelope2)
    wb.addRow(weight=397, arm=1.908)
    wb.addRow(weight=185, arm=1.800)
    wb.addRow(weight=28.8, arm=2.209)
    wb.addRow(weight=15, arm=2.417)

    rawimage = wb.plot()
    with open('wnb.png', 'w') as f:
        f.write(base64.b64decode(rawimage))
