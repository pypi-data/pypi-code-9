import os
import tempfile

PXM_S3_PREFIX = "s3://mapbox-pxm/"
PXM_SOURCES_PREFIX = "s3://mapbox/pxm-sources/master/"


class PxmFile(object):
    @staticmethod
    def getfile(pxm_filename):
        if PxmFile.isSceneFile(pxm_filename):
            return SceneFile(pxm_filename)

    @staticmethod
    def isSceneFile(pxm_filename):
        if len(pxm_filename.split('-')) == 6:
            return True
        return False


class SceneFile(PxmFile):
    pxm_filetype = "scene_file"
    """
    based on specs for scene-tiffs outlined here
    https://github.com/mapbox/pxm#scenetiff-spec--draft
    """

    def __init__(self, pxm_filename):
        self.scene_file = os.path.basename(pxm_filename)
        split_name = self.scene_file.split('-')
        self.zoom = int(split_name[0])
        self.coord_x = int(split_name[1])
        self.coord_y = int(split_name[2])
        self.source_id = split_name[3]
        self.date = split_name[4]
        self.srcimg_id = split_name[5].split('.')[0]
        self.extension = split_name[5].split('.')[1]
        self.layer_name = None

    def printInfo(self):
        print("Z-X-Y: %d-%d-%d" % (self.zoom, self.coord_x, self.coord_y))
        print("source_id: %s" % self.source_id)
        print("srcimg_id: %s" % self.srcimg_id)

    def getZXY(self):
        return ("%d-%d-%d" % (self.zoom, self.coord_x, self.coord_y))

    def getXYZlist(self):
        """
        return as list of [X, Y, Z]
        """
        return [self.coord_x, self.coord_y, self.zoom]

    def getSourceid(self):
        return ("%s" % self.source_id)

    def getSourceImg(self):
        return("%s" % self.srcimg_id)

    def _getLayerName(self):
        """
        look on s3 in 'pxm-sources' to find the layer name
        - not reliable, need more of a spec sheet13-4096-3071
        """
        if self.layer_name:
            return self.layer_name

        layer_filepath = os.path.join(PXM_SOURCES_PREFIX, self.source_id, 'layers')
        temp_file = tempfile.gettempdir() + "/%s_layer" % self.source_id

        if not os.path.exists(temp_file):
            cmd = 'aws s3 cp %s %s' % (layer_filepath, temp_file)
            os.system(cmd)
        f = open(temp_file, 'r')
        layer_name = f.read().lstrip().rstrip()

        self.layer_name = layer_name
        return self.layer_name

    def predictLayerTifPath(self):
        layer_name = self._getLayerName()
        return os.path.join(PXM_S3_PREFIX, 'layers', layer_name, "%s-%s-%s.tif")

    def predictLayerTimePath(self):
        layer_name = self._getLayerName()
        return os.path.join(PXM_S3_PREFIX, 'layers', layer_name, "%s-%s-%s.time")
