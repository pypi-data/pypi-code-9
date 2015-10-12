import os
import json
from StringIO import StringIO
import click
import pxmfile
"""
parses the checker output into a zxy lists
the raw watchbot checker output from s3 looks like this:

corss reference against edge tiles list

this script reads a whole directory of them and outputs them into two files, 
- one of missing zxy and 
- one of nodata zxy
"""


class CheckerParser:
    """
    parses the output of checker
    """
    def __init__(self, sourceid, edgefile=None, checkeroutput_raw=None, allscenegeojson_file=None, output_dir=None):
        self.sourceid = sourceid
        self.checkeroutput_raw = checkeroutput_raw
        self.output_dir = output_dir
        self.edgefile = edgefile

        self.allscenegeojson_file = allscenegeojson_file

        # keep a record of all the files written by this script
        self.outputfiles_dict = {}

        # file containing all the scenetifs
        # read the edge file list

        self.edge_tiles_list = []
        if self.edgefile:
            self.readEdgeList()

        self.raw_nodata = []
        self.raw_missing = []
        self.readCheckerFile()
        self.printProblemZXY()

        self.findSourceImages()

    def parseURLtoZXY(self, urlpath):
        """
        parses the z-x-y out a mapbox tile url that looks like:
        https://api.mapbox.com/v4/mapid.my-map/13/7346/4310.png?access_token=<pk.e8QWfLg>
        """
        spliturl = urlpath.split('/')
        z = spliturl[5]
        x = spliturl[6]
        y = spliturl[7].split('.')[0]

        if (z.isdigit() and y.isdigit() and x.isdigit()) == False:
            return None

        return "%s-%s-%s" % (z, x, y)

    def readEdgeList(self):
        """
        reads a list of zxys that are on the edge
        """
        with open(self.edgefile, 'r') as ef:
            for line in ef:
                self.edge_tiles_list.append(line.lstrip().rstrip())

    def findSourceImages(self):
        """
        match 'Z-X-Y' strings to their respective source images
        """

        zxy_to_srcimg_dict = {}
        source_images_to_retouch = []

        with open(self.allscenegeojson_file, 'r') as scenels:
            for line in scenels:
                pxmf = pxmfile.PxmFile.getfile(line.lstrip().rstrip())
                zxy_to_srcimg_dict[pxmf.getZXY()] = pxmf.getSourceImg()

        for zxy in self.raw_missing:
            if zxy_to_srcimg_dict[zxy] not in source_images_to_retouch:
                source_images_to_retouch.append(zxy_to_srcimg_dict[zxy])

        for zxy in self.raw_nodata:
            if zxy_to_srcimg_dict[zxy] not in source_images_to_retouch:
                source_images_to_retouch.append(zxy_to_srcimg_dict[zxy])

        output_sourceimgs = os.path.join(self.output_dir, "%s_missing_and_nodata_sourceimgs" % (self.sourceid))
        with open(output_sourceimgs, 'w') as output:
            for srcimg in source_images_to_retouch:
                output.write(srcimg+"\n")

    def readCheckerFile(self):
        with open(self.checkeroutput_raw, 'r') as checker_file:
            for line in checker_file:
                io = StringIO(line)
                tilejson = json.load(io)
                zxystring = self.parseURLtoZXY(tilejson['tile'])

                # some of the checker urls have bad ZXY coords
                if zxystring in self.edge_tiles_list or not zxystring:
                    continue

                if tilejson.has_key('missingTile'):
                    self.raw_missing.append(zxystring)
                if tilejson.has_key('missingCorners'):
                    self.raw_nodata.append(zxystring)

    def printProblemZXY(self):

        output_all = os.path.join(self.output_dir, "%s_missing_and_nodata_zxy" % (self.sourceid))
        output_nodata = os.path.join(self.output_dir, "%s_nodata_zxy" % (self.sourceid))
        output_missing = os.path.join(self.output_dir, "%s_missing_zxy" % (self.sourceid))

        allout_file = open(output_all, 'w')
        nodata_file = open(output_nodata, 'w')
        missing_file = open(output_missing, 'w')

        for missingzxy in self.raw_missing:
            allout_file.write(missingzxy + '\n')
            missing_file.write(missingzxy + '\n')

        for nodatazxy in self.raw_nodata:
            allout_file.write(nodatazxy+"\n")
            nodata_file.write(nodatazxy+"\n")

        allout_file.close()
        nodata_file.close()
        missing_file.close()


@click.command()
@click.option('--s3parsejson', default="0", help='json file with necessary specs for this mosaic')
@click.option('--checkeroutput', default="0", help='checker outputs collected into a text file of json entries')
def checkerParser(s3parsejson, checkeroutput):
    with open(s3parsejson, 'r') as s3outputsfile:
        s3outputs = json.loads(s3outputsfile.read())

    edge_zxy_file = s3outputs['zxy_edge_list']
    sourceid = s3outputs['sourceid']
    output_dir = s3outputs['output_dir']
    allscenegeojson_file = s3outputs['all_tile_geojsons']

    checker = CheckerParser(sourceid, edge_zxy_file, checkeroutput, allscenegeojson_file,  output_dir)


if __name__ == '__main__':
    checkerParser()
