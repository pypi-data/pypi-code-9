import click
import os
import json
from tempfile import NamedTemporaryFile
import rasterio
import multiprocessing
import functools
import mercantile

try:
    # python 3
    from urllib.request import urlopen as urlopen
except:
    # python 2
    from urllib import urlopen as urlopen

mapbox_access_token = os.environ.get("MapboxAccessToken")


class SingleTileCheck:
    """
    checks a single tile
    """
    def __init__(self, mapID, tilezxy, mb_access_token=None):
        self.mapID = mapID
        self.tilezxy = tilezxy

        self.mapbox_access_token = None
        if mb_access_token:
            self.mapbox_access_token = mb_access_token
        elif mapbox_access_token:
            self.mapbox_access_token = mapbox_access_token
        else:
            raise AttributeError("no valid access token given")

    def getTile(self, zxy):
        """
        Get tile from Mapbox API, write to a temporary file.
        """

        tmp = NamedTemporaryFile()
        img = urlopen("https://api.mapbox.com/v4/{mapID}/{z}/{x}/{y}.png?access_token={token}".format(mapID=self.mapID, z=zxy[0], x=zxy[1], y=zxy[2], token=self.mapbox_access_token))

        if img.getcode() != 200:
            tmp.close()
            return None, img.getcode()

        with open(tmp.name, "wb") as tmpFile:
            tmpFile.write(img.read())

        return tmp, None

    def checkCorners(self, img):
        """
        Returns alpha channel values for four corners of a file.
        """

        x = [0, img.width - 1]
        y = [0, img.height - 1]
        corners = [[a, b] for a in x for b in y]
        data = img.read()[3]
        alphas = map(lambda x: data[x[0]][x[1]], corners)
        return alphas

    def checkTile(self):
        """
        Checks an individual tile for HTTP errors and nodata corners.
        Returns [alpha count, HTTP error code]
        """
        zxy = self.tilezxy
        img, error = self.getTile(zxy)

        tileout_dict = {}
        tileout_dict['zxy'] = self.tilezxy
        tileout_dict['HTTPerror'] = None
        tileout_dict['nodata'] = None

        if error and not img:
            tileout_dict['HTTPerror'] = error
            return tileout_dict

        with rasterio.open(img.name) as src:
            alphas = self.checkCorners(src)
            img.close()
            tileout_dict['nodata'] = alphas.count(0)
            return tileout_dict


def checkTileFunc(mapid, mb_access_token, zxy):
    tc = SingleTileCheck(mapid, zxy, mb_access_token)
    return tc.checkTile()


class TileChecker:
    """
    Class to check tile list.
    Takes arguments (mapID, path-to-tile-file)
    Writes bad tile list to a file suffixed '.bad'
    """
    def __init__(self, mapID, tilefile, outfile=None, mb_access_token=None):
        self.mapID = mapID
        self.tilefile = tilefile
        self.tiles = self.parseTiles
        self.mapbox_access_token = mb_access_token
        self.outfile = outfile

        self.badtiles = []

    @property
    def parseTiles(self):
        """
        Parses file of 'z-x-y' lines into array of [z,x,y]
        """

        return [map(int, line.rstrip('\n').split('-')) for line in open(self.tilefile)]

    def findBadTiles(self):
        """
        Given list of tiles, return a list of bad (HTTP error or nodata count) tiles
        """
        procs = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=procs)
        with rasterio.drivers():
            tileCheckPartial = functools.partial(checkTileFunc, self.mapID, self.mapbox_access_token)
            badtiles = pool.map(tileCheckPartial, self.tiles)

        self.badtiles = badtiles

    def outputToFile(self):
        """
        Writes bad tile list to file, suffixed '.bad'
        """
        output = self.tilefile + '.bad'
        if self.outfile:
            output = self.outfile

        with open(output, 'wb') as outfile:
            for tile in self.badtiles:
                outfile.write('%s\n' % str(tile))

    def _ZXYtoFeature(self, tile):
        z = tile[0]
        x = tile[1]
        y = tile[2]

        bounds = mercantile.bounds(x, y, z)
        coords = [
            [bounds.west, bounds.south],
            [bounds.west, bounds.north],
            [bounds.east, bounds.north],
            [bounds.east, bounds.south],
            [bounds.west, bounds.south]
        ]

        feature = {}
        feature['type'] = 'Feature'
        feature['properties'] = {
            'tile': [x, y, z]
        }
        feature['geometry'] = {
            'type': 'Polygon',
            'coordinates': [coords]
        }

        return feature

    def outputGeojson(self, outputfile_path=None):
        """
        ouputs bad files in geojson
        """
        output = {}
        output['type'] = 'FeatureCollection'
        output['features'] = []

        if outputfile_path == None:
            outputfile_path = self.tilefile + "_missingNodata.geojson"

        for tile_dict in self.badtiles:
            # print "looking at tilestr" + tilestr
            # tile_dict = eval(str(tilestr))
            if tile_dict['HTTPerror'] or tile_dict['nodata']:
                feature = self._ZXYtoFeature(tile_dict['zxy'])
                output['features'].append(feature)

        writeout = json.dumps(output, separators=(',', ':'))
        with open(outputfile_path, 'w') as f_out:
            f_out.write(writeout)

        return outputfile_path


@click.command()
@click.option('--tilelist', default="0", help='zxy list of tiles to check')
@click.option('--mapid', default="0", help='mapid of map to check')
def check_tiles(tilelist, mapid):

    tileChecker = TileChecker(mapid, tilelist)
    tileChecker.findBadTiles()
    tileChecker.outputToFile()

if __name__ == '__main__':
    check_tiles()
