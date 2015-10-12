import click
import numpy
from scipy import ndimage


class EdgeFinder:
    """
    class to find objects
    """
    def __init__(self, inzxy, outzxy, zoomlevel):
        self.inzxy = inzxy
        self.outzxy = outzxy
        self.zoomlevel = zoomlevel

        self.edge_xy_list = []

    def findEdges(self):
        # read zxy list and find min/max x&y
        self.source_zxy_coords, self.max_x, self.max_y, self.min_x, self.min_y = self.readZXYFile(self.inzxy)

        # create the matrix to plot the tile coords
        self.map_size = (self.max_x-self.min_x+1, self.max_y-self.min_y+1)
        # self.map_zxy_matrix = numpy.zeros(map_size)

        self.map_zxy_matrix = self.populateMatrix(self.map_size, self.source_zxy_coords)
        self.map_zxy_matrix_eroded = ndimage.binary_erosion(self.map_zxy_matrix).astype(self.map_zxy_matrix.dtype)

        for tile in self.source_zxy_coords:
            matrixcoord = self.ZXYtoMatrix(tile)
            x = matrixcoord[0]
            y = matrixcoord[1]
            if (self.map_zxy_matrix[x][y] == 1) and (self.map_zxy_matrix_eroded[x][y] == 0):
                self.edge_xy_list.append(tile)

    def writeFile(self):
        """
        write out the found edges list to an output file
        """

        outfile = open(self.outzxy, 'w')
        zoom = 13
        for coord in self.edge_xy_list:
            outfile.write("%d-%d-%d\n" % (zoom, coord[0], coord[1]))
        outfile.close()

        return self.outzxy

    def populateMatrix(self, map_size, zxy_list):
        """
        input: zxy_list - a list of zxy based on the file input
            - map_size - size of the map based on max/min values of x and y coordinates
            - output: a matrix with '1' at XY tile coords where there are tiles
        """
        # create the matrix to plot the tile coords
        map_zxy_matrix = numpy.zeros(map_size)

        for t in zxy_list:
            mc = self.ZXYtoMatrix(t)  # matri_coord
            map_zxy_matrix[mc[0]][mc[1]] = 1

        return map_zxy_matrix

    def matrixToZXY(self, matrixCoord):
        """
        converts from matrix xy space to zxy space
        """
        return (matrixCoord[0] + self.min_x, matrixCoord[1] + self.min_y)

    def ZXYtoMatrix(self, tileCoord):
        """
        converts from tile ZXY space to matrix XY space
        """
        return (tileCoord[0] - self.min_x, tileCoord[1] - self.min_y)

    def readZXYFile(self, zxy_file=None):
        """
        reads zxy file
        creates min/max ZX to set at space for new grid
        also a list of (int x, int y) coords
        """

        if zxy_file == None:
            zxy_file == self.inzxy

        fileObj = open(zxy_file)

        l = fileObj.readline()
        zxylist = l.lstrip().rstrip().split('-')

        x = int(zxylist[1])
        y = int(zxylist[2])

        min_x = max_x = x
        min_y = max_y = y

        source_zxy_coords = [(x, y)]

        for l in fileObj:
            zxylist = l.lstrip().rstrip().split('-')

            x = int(zxylist[1])
            y = int(zxylist[2])
            source_zxy_coords.append((x, y))
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y

        # return source_zxy_coords
        click.echo("max x: %d" % max_x)
        click.echo("max y: %d" % max_y)
        click.echo("min x: %d" % min_x)
        click.echo("min y: %d" % min_y)
        return source_zxy_coords, max_x, max_y, min_x, min_y


@click.command()
@click.argument("inzxy", type=click.Path(exists=True))
@click.argument("outzxy", type=click.Path(exists=False))
@click.argument('zoom', type=int, metavar='z', default=13)
def get_files(inzxy, outzxy, zoom):
    edgeFinder = EdgeFinder(inzxy, outzxy, zoom)
    edgeFinder.findEdges()
    edgeFinder.writeFile()

if __name__ == '__main__':
    get_files()
