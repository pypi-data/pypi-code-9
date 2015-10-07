"""A script to drive testing of pygeoprocessing as we make updates to it, can
be deleted once refactor is complete."""

import unittest
import logging

from osgeo import osr
from osgeo import gdal
import pygeoprocessing
import cProfile
import pstats

BASE_CELL_SIZE = 30

class PygeoProcessingTest(unittest.TestCase):

    def test_align_raster_list(self):
        raster_path_list = [
            r"C:\Users\Rich\Documents\svn_repos\invest-sample-data\Base_Data\Freshwater\landuse_90",
            r"C:\Users\Rich\Documents\svn_repos\invest-sample-data\Base_Data\Freshwater\dem",
            ]
        raster_out_path_list = ['1.tif', '2.tif']
        resample_method_list = ['bilinear'] *2
        raster_to_align_index = 1
        #aoi_path = r"C:\Users\Rich\Documents\svn_repos\invest-sample-data\Base_Data\Freshwater\subwatersheds.shp"
        aoi_path = None
        #aoi_metadata = pygeoprocessing.get_vector_metadata(aoi_path)
        #print aoi_metadata
        mode = 'raster'
        pygeoprocessing.align_raster_list(
            raster_path_list, resample_method_list,
            BASE_CELL_SIZE, mode, raster_out_path_list,
            raster_to_align_index=raster_to_align_index, aoi_path=aoi_path,
            assert_rasters_projected=False, all_touched=False)
        pygeoprocessing.create_simple_raster_attribute_table(
            raster_out_path_list[0], {1: 'baz', 2: 'bar'}, 'names')

        rat = pygeoprocessing.get_raster_attribute_table(
            raster_out_path_list[0], band_index=1)

    def test_resize_resample_raster(self):
        base_raster_path = r"C:\Users\Rich\Dropbox\cold_storage_dont_delete\global_precip.tiff"
        metadata = pygeoprocessing.get_raster_metadata(base_raster_path)
        clip_raster_path = r"C:\Users\Rich\Dropbox\cold_storage_dont_delete\af_biov2ct1.tif"
        out_pixel_size = 50000
        resample_method = 'bilinear'
        out_path = 'resample.tif'
        clip_metadata = pygeoprocessing.get_raster_metadata(clip_raster_path)
        pygeoprocessing.resize_resample_raster(
            base_raster_path, clip_metadata['bounding_box'], out_pixel_size,
            resample_method, out_path)
        metadata = pygeoprocessing.get_raster_metadata(out_path)

    def test_extract_datasource_table_by_key(self):
        shapefile_uri = r"C:\Users\Rich\Documents\svn_repos\invest-sample-data\Base_Data\Freshwater\subwatersheds.shp"
        table = pygeoprocessing.extract_datasource_table_by_key(shapefile_uri, None)
        table = pygeoprocessing.extract_datasource_table_by_key(shapefile_uri, 'subws_id')


    def test_aggregate_raster_values(self):
        big_raster_path = r"C:\Users\Rich\Documents\svn_repos\invest-sample-data\Base_Data\Freshwater\landuse_90"
        shapefile_path = r"C:\Users\Rich\Documents\svn_repos\invest-sample-data\Base_Data\Freshwater\subwatersheds.shp"

        result = pygeoprocessing.aggregate_raster_values(
            big_raster_path, shapefile_path, shapefile_field='subws_id',
            ignore_nodata=True, threshold_amount_lookup=None, ignore_value_list=[],
            all_touched=False)


    def test_interpolate(self):
        point_shapefile_path = r"C:\Users\Rich\Documents\svn_repos\invest-sample-data\MarineWaterQuality\input\floathomes_centroids.shp"
        output_path = 'interpolate_points.tif'
        pygeoprocessing.create_raster_from_vector_extents(
            point_shapefile_path, BASE_CELL_SIZE, gdal.GDT_Float32, -1, output_path)
        pygeoprocessing.interpolate_point_data(
            point_shapefile_path, 'Id', 'linear', output_path)

    def test_raster_from_vector(self):
        shapefile_uri = r"C:\Users\Rich\Documents\svn_repos\invest-sample-data\Base_Data\Freshwater\subwatersheds.shp"
        gdal_format = gdal.GDT_Float32
        nodata = -1.0
        output_uri = 'raster_from_vector.tif'
        pygeoprocessing.create_raster_from_vector_extents(
            shapefile_uri, BASE_CELL_SIZE, gdal_format, nodata, output_uri)
        output_uri = 'multiband_rect_raster_from_vector.tif'
        pygeoprocessing.create_raster_from_vector_extents(
            shapefile_uri, BASE_CELL_SIZE, gdal_format, nodata, output_uri, n_bands=5)

    def test_reproject_raster(self):
        base_raster_path = r"C:\Users\Rich\Documents\svn_repos\invest-sample-data\Base_Data\Freshwater\dem"
        out_path = 'reprojected_raster.tif'
        out_sr = osr.SpatialReference()
        out_sr.ImportFromEPSG(32149)  # south washington
        pygeoprocessing.reproject_raster(
            base_raster_path, BASE_CELL_SIZE, out_sr.ExportToWkt(), 'nearest',
            out_path)

    def test_reproject_vector(self):
        base_vector_path = r"C:\Users\Rich\Documents\svn_repos\invest-sample-data\forest_carbon_edge_effect\core_data\forest_carbon_edge_regression_model_parameters.shp"
        base_raster_path = r"C:\Users\Rich\Documents\svn_repos\invest-sample-data\Base_Data\Freshwater\landuse_90"
        out_path = 'reprojected_vector.shp'
        base_metadata = pygeoprocessing.get_raster_metadata(base_raster_path)
        out_projection = base_metadata['projection']

        pygeoprocessing.reproject_vector(
            base_vector_path, out_projection, out_path)

    def test_raster_local_op(self):
        """Runs a vectorize datasets call so we can wrap it up to profile"""
        big_raster_filename = r"C:\Users\Rich\Documents\svn_repos\invest-sample-data\Base_Data\Freshwater\landuse_90"
        #aoi_path = r"C:\Users\Rich\Documents\svn_repos\invest-sample-data\Base_Data\Freshwater\watersheds.shp"
        aoi_path = None

        def add_op(x, y):
            """adds two rasters"""
            return x + y
        out_path = 'run_vd_test.tif'
        metadata = pygeoprocessing.get_raster_metadata(big_raster_filename)
        nodata = metadata['nodata']
        pygeoprocessing.raster_local_op(
            [(big_raster_filename, 1), big_raster_filename], add_op,
            gdal.GDT_Float32, nodata[0] * 2, BASE_CELL_SIZE, "intersection",
            out_path, aoi_path=aoi_path)

        #print pygeoprocessing.get_raster_metadata(big_raster_filename)

    def test_reclass_and_lookup(self):
        table_path = r"C:\Users\Rich\Documents\svn_repos\invest-sample-data\Base_Data\Freshwater\biophysical_table.csv"
        table = pygeoprocessing.get_lookup_from_table(table_path, 'lucode')
        big_raster_filename = r"C:\Users\Rich\Documents\svn_repos\invest-sample-data\Base_Data\Freshwater\landuse_90"

        value_map = dict([
            (lucode, val['usle_c']) for lucode, val in table.iteritems()])
        out_path = 'landuse90_usle_c.tif'
        out_nodata = -9999
        pygeoprocessing.reclassify_raster(
            big_raster_filename, value_map, gdal.GDT_Float32, out_nodata, out_path,
            exception_flag='values_required')


if __name__ == '__main__':
    cProfile.run('unittest.main()', 'stats')
    p = pstats.Stats('stats')
    p.sort_stats('time').print_stats(10)
#    p.sort_stats('cumulative').print_stats(10)
