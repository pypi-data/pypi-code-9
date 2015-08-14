from fipy.tools import numerix
from matplotlib.collections import PolyCollection


class VarPlot(object):

    def __init__(self, var, cmap, axes):
        self.axes = axes
        self.var = var
        self.cmap = cmap
        self.mesh = self.var.mesh
        self.plot_mesh()

    def plot_mesh(self):
        vertexIDs = self.mesh._orderedCellVertexIDs
        vertexCoords = self.mesh.vertexCoords
        xCoords = numerix.take(vertexCoords[0], vertexIDs)
        yCoords = numerix.take(vertexCoords[1], vertexIDs)
        polys = []
        for x, y in zip(xCoords.swapaxes(0, 1), yCoords.swapaxes(0, 1)):
            polys.append(zip(x, y))
        self.collection = PolyCollection(polys)
        self.collection.set_linewidth(0.5)
        self.axes.add_collection(self.collection)
        self.update(self.var)

    def update(self, var):
        rgba = self.cmap(var.value)
        self.collection.set_facecolors(rgba)
        self.collection.set_edgecolors(rgba)
