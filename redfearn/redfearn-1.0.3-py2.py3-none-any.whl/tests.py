# Copyright 2015, Phil Howarth (phil@plaintech.net.au)
#
# This file is part of Australian NTv2 Grid Conversion.
#
# Australian NTv2 Grid Conversion is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Australian NTv2 Grid Conversion is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Australian NTv2 Grid Conversion.  If not, see <http://www.gnu.org/licenses/>.

import redfearn
import unittest


class KnownValues(unittest.TestCase):
    dms_test_values = [
        [redfearn.DMS(-37, 39, 10.15611), -37.652821141666664],
        [redfearn.DMS(143, 55, 35.38393), 143.9264955361111],
        [redfearn.DMS(127, 10, 25.07), 127.17363055555556],
        [redfearn.DMS(-1, 52, 43.22), -1.8786722222222223],
        [redfearn.DMS(125, 17, 41.86), 125.2949611111111],
        [redfearn.DMS(0, 0, -20.67), -0.0057416666666666675],
        [redfearn.DMS(125, 17, 21.18), 125.28921666666666],
        [redfearn.DMS(0, 18, 19.70), 0.3054722222222222],
        [redfearn.DMS(0, 0, 40.14), 0.01115],
        [redfearn.DMS(-37, 57, 03.72030), -37.95103341666667],
        [redfearn.DMS(144, 25, 29.52442), 144.42486789444445],
        [redfearn.DMS(306, 52, 05.37), 306.8681583333333],
        [redfearn.DMS(-1, 35, 03.65), -1.5843472222222224],
        [redfearn.DMS(305, 17, 01.72), 305.28381111111116],
        [redfearn.DMS(0, 0, 19.47), 0.005408333333333333],
        [redfearn.DMS(305, 17, 21.18), 305.2892166666667],
        [redfearn.DMS(0, 0, 0), 0],
        [redfearn.DMS(60, 0, 0), 60],
        [redfearn.DMS(0, 60, 0), 1],
        [redfearn.DMS(0, 0, 60), 0.016666666666666666],
        [redfearn.DMS(-0, 0, 0), 0],
        [redfearn.DMS(-60, 0, 0), -60],
        [redfearn.DMS(0, -60, 0), -1],
        [redfearn.DMS(0, 0, -60), -0.016666666666666666],
    ]

    known_values = [
        {
            'name': 'Buninyong',
            'data': {
                'latitude_dms': redfearn.DMS(-37, 39, 10.15611),
                'longitude_dms': redfearn.DMS(143, 55, 35.38393),
                'ahd': 744.986,
                'n_ausgeoid98': 4.869,
                'ellipsoidal_height': 749.855,
                'coordinate_system': "GDA-MGA",
                'easting': 228854.052,
                'northing': 5828259.038,
                'zone': 55,
                'x': -4087103.458,
                'y': 2977473.0435,
                'z': -3875464.7525,
                'azimuth_dms': redfearn.DMS(127, 10, 25.07),
                'grid_convergence_dms': redfearn.DMS(-1, 52, 43.22),
                'grid_bearing_dms': redfearn.DMS(125, 17, 41.86),
                'arc_to_chord_dms': redfearn.DMS(0, 0, -20.67),
                'plane_bearing_dms': redfearn.DMS(125, 17, 21.18),
                'point_scale_factor': 1.00050567,
                'meridian_distance': -4173410.326,
                'rho': 6359253.8294,
                'nu': 6386118.6742,
                'ellipsoidal_distance': 54972.271,
                'line_scale_factor': 1.00036397,
                'grid_and_plane_distance': 54992.279,
                'meridian_convergence_dms': redfearn.DMS(0, 18, 19.70),
                'line_curvature_dms': redfearn.DMS(0, 0, 40.14)
            }
        },
        {
            'name': 'Buninyong',
            'data': {
                'latitude_dms': redfearn.DMS(-37, 39, 10.15611),
                'longitude_dms': redfearn.DMS(143, 55, 35.38393),
                'ahd': 744.986,
                'n_ausgeoid98': 4.869,
                'ellipsoidal_height': 749.855,
                'coordinate_system': "GDA-MGA",
                'easting': 758173.798008,
                'northing': 5828674.33973,
                'zone': 54,
                'x': -4087103.458,
                'y': 2977473.0435,
                'z': -3875464.7525,
                'azimuth_dms': redfearn.DMS(127, 10, 25.07),
                'grid_convergence_dms': redfearn.DMS(1, 47, 19.360430267999618),
                'grid_bearing_dms': redfearn.DMS(125, 17, 41.86),
                'arc_to_chord_dms': redfearn.DMS(0, 0, -20.67),
                'plane_bearing_dms': redfearn.DMS(125, 17, 21.18),
                'point_scale_factor': 1.00042107306,
                'meridian_distance': -4173410.326,
                'rho': 6359253.8294,
                'nu': 6386118.6742,
                'ellipsoidal_distance': 54972.271,
                'line_scale_factor': 1.00036397,
                'grid_and_plane_distance': 54992.279,
                'meridian_convergence_dms': redfearn.DMS(0, 18, 19.70),
                'line_curvature_dms': redfearn.DMS(0, 0, 40.14)
            }
        },
        {
            'name': 'Flinders Peak',
            'data': {
                'latitude_dms': redfearn.DMS(-37, 57, 03.72030),
                'longitude_dms': redfearn.DMS(144, 25, 29.52442),
                'ahd': 347.200,
                'n_ausgeoid98': 3.748,
                'ellipsoidal_height': 350.948,
                'coordinate_system': "GDA-MGA",
                'easting': 273741.297,
                'northing': 5796489.777,
                'zone': 55,
                'x': -4096088.424,
                'y': 2929823.08435,
                'z': -3901375.4540,
                'azimuth_dms': redfearn.DMS(306, 52, 05.37),
                'grid_convergence_dms': redfearn.DMS(-1, 35, 03.65),
                'grid_bearing_dms': redfearn.DMS(305, 17, 01.72),
                'arc_to_chord_dms': redfearn.DMS(0, 0, 19.47),
                'plane_bearing_dms': redfearn.DMS(305, 17, 21.18),
                'point_scale_factor': 1.00023056,
                'meridian_distance': -4205192.300,
                'rho': 6359576.5731,
                'nu': 6386226.7080,
                'ellipsoidal_distance': 54972.271,
                'line_scale_factor': 1.00036397,
                'grid_and_plane_distance': 54992.279,
                'meridian_convergence_dms': redfearn.DMS(0, 18, 19.70),
                'line_curvature_dms': redfearn.DMS(0, 0, 40.14)
            }
        }
    ]

    # def test_decdeg2dms(self):
    #    """ Test the decimal degree to dms conversion
    #    """
    #    for i in self.dms_test_values:
    #        self.assertEqual(redfearn.decdeg2dms(i[1]), i[0])

    def test_dms2decdeg(self):
        """ Test the dms to decimal degrees conversion
        """
        for i in self.dms_test_values:
            self.assertEqual(redfearn.dms2decdeg(i[0]), i[1])

    def test_dms2decdeg_and_decdeg2dms_cycle(self):
        """ Test the dms to decimal conversion by cycling between the two.

            dms2decdeg and decdeg2dms should cycle accurately between values without variation
            there is occasionally variation between the initial dms seconds value and the second
            cycle due to floating point errors but the decimal expansion should be identical to at least 12 decimal places

            There can also be variations due to different valid dms values, e.g. 0 deg, 60 min, 0 sec is 1.0 degrees
            or could also be written as 1 deg, 0 min, 0 sec.
        """
        for i in self.dms_test_values:
            dd1 = redfearn.dms2decdeg(i[0])
            dms2 = redfearn.decdeg2dms(dd1)
            dd2 = redfearn.dms2decdeg(dms2)
            self.assertAlmostEqual(dd1, dd2, 12)

    def test_latlon2grid_conversion(self):
        """ Test the latlon2grid conversion.

            eastings and northings should be within 1 millimetre of known values
            grid_convergence is tested to 5 decimal places
            point_scale_factor is tested to 8 decimal places
        """
        for known_site in self.known_values:
            latitude_dd = redfearn.dms2decdeg(known_site['data']['latitude_dms'])
            longitude_dd = redfearn.dms2decdeg(known_site['data']['longitude_dms'])
            grid = redfearn.latlon2grid(latitude_dd, longitude_dd, known_site['data']['coordinate_system'], zone=known_site['data']['zone'])
            self.assertAlmostEqual(grid['easting'], known_site['data']['easting'], delta=0.001)
            self.assertAlmostEqual(grid['northing'], known_site['data']['northing'], delta=0.001)
            self.assertEqual(grid['zone'], known_site['data']['zone'])
            self.assertAlmostEqual(grid['grid_convergence'], redfearn.dms2decdeg(known_site['data']['grid_convergence_dms']), 5)
            self.assertAlmostEqual(grid['point_scale_factor'], known_site['data']['point_scale_factor'], 8)

    def test_grid2latlon_conversion(self):
        """ Test the grid2latlon conversion.

            eastings and northings should be within 1 millimetre of known values
            grid_convergence is tested to 5 decimal places
            point_scale_factor is tested to 8 decimal places
        """
        for known_site in self.known_values:
            latlon = redfearn.grid2latlon(
                known_site['data']['easting'],
                known_site['data']['northing'],
                known_site['data']['zone'],
                coordinate_system=known_site['data']['coordinate_system']
            )
            self.assertAlmostEqual(latlon['latitude'], redfearn.dms2decdeg(known_site['data']['latitude_dms']), 8)
            self.assertAlmostEqual(latlon['longitude'], redfearn.dms2decdeg(known_site['data']['longitude_dms']), 8)
            self.assertAlmostEqual(latlon['grid_convergence'], redfearn.dms2decdeg(known_site['data']['grid_convergence_dms']), 5)
            self.assertAlmostEqual(latlon['point_scale_factor'], known_site['data']['point_scale_factor'], 8)

    def test_latlon2grid_and_grid2latlon_cycle(self):
        """ Test that converting from lat/lon to grid and back to lat/lon occurs correctly.

            eastings and northings should be within 1 millimetre of known values
            grid_convergence is tested to 5 decimal places
            point_scale_factor is tested to 8 decimal places
        """
        for known_site in self.known_values:
            latitude_dd = redfearn.dms2decdeg(known_site['data']['latitude_dms'])
            longitude_dd = redfearn.dms2decdeg(known_site['data']['longitude_dms'])
            grid = redfearn.latlon2grid(latitude_dd, longitude_dd, 'GDA-MGA', zone=known_site['data']['zone'])
            latlon = redfearn.grid2latlon(
                grid['easting'],
                grid['northing'],
                grid['zone'],
                coordinate_system=known_site['data']['coordinate_system']
            )
            self.assertAlmostEqual(latlon['latitude'], redfearn.dms2decdeg(known_site['data']['latitude_dms']), 8)
            self.assertAlmostEqual(latlon['longitude'], redfearn.dms2decdeg(known_site['data']['longitude_dms']), 8)
            self.assertAlmostEqual(latlon['grid_convergence'], redfearn.dms2decdeg(known_site['data']['grid_convergence_dms']), 5)
            self.assertAlmostEqual(latlon['point_scale_factor'], known_site['data']['point_scale_factor'], 8)

    def test_grid2latlon_and_latlon2grid_cycle(self):
        """ Test that converting from grid to lat/lon and back to grid occurs correctly.

            eastings and northings should be within 1 millimetre of known values
            grid_convergence is tested to 5 decimal places
            point_scale_factor is tested to 8 decimal places
        """
        for known_site in self.known_values:
            latlon = redfearn.grid2latlon(
                known_site['data']['easting'],
                known_site['data']['northing'],
                known_site['data']['zone'],
                coordinate_system=known_site['data']['coordinate_system']
            )
            grid = redfearn.latlon2grid(latlon['latitude'], latlon['longitude'], known_site['data']['coordinate_system'], zone=known_site['data']['zone'])
            self.assertAlmostEqual(grid['easting'], known_site['data']['easting'], delta=0.001)
            self.assertAlmostEqual(grid['northing'], known_site['data']['northing'], delta=0.001)
            self.assertEqual(grid['zone'], known_site['data']['zone'])
            self.assertAlmostEqual(grid['grid_convergence'], redfearn.dms2decdeg(known_site['data']['grid_convergence_dms']), 5)
            self.assertAlmostEqual(grid['point_scale_factor'], known_site['data']['point_scale_factor'], 8)

if __name__ == '__main__':
    unittest.main()