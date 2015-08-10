from __future__ import print_function, division
import numpy as np
from ahoy import turners
from ciabatta.vector import smallest_signed_angle as angle_dist
import test


class TestTurner(test.TestBase):
    turner_cls = turners.Turner
    left = np.pi
    right = 0.0
    up = np.pi / 2.0
    down = -np.pi / 2.0

    NE = np.pi / 4.0
    NW = 3.0 * np.pi / 4.0
    SW = -3.0 * np.pi / 4.0
    SE = -np.pi / 4.0

    def setUp(self):
        super(TestTurner, self).setUp()
        self.turner = self.turner_cls()

    def do_turning(self, th_normal, th_in, th_out_expected):
        print('Normal: {:g}'.format(th_normal))
        print('In: {:g}'.format(th_in))
        th_in = np.array([th_in])
        th_normal = np.array([th_normal])
        th_out = self.turner.get_norm_angle(th_in, th_normal, self.rng)
        print('Out: {:g}'.format(th_out[0]))
        print('Expected: {:g}'.format(th_out_expected))
        self.assertTrue(np.allclose(angle_dist(th_out, th_out_expected), 0.0))

    def test_right_left(self):
        self.do_turning(self.left, self.right, self.right)

    def test_up_left(self):
        self.do_turning(self.left, self.up, self.up)

    def test_down_left(self):
        self.do_turning(self.left, self.down, self.down)

    def test_equivalent_angles(self):
        th_in = self.NE
        th_in = np.array([th_in])
        th_outs = []
        for i in range(-2, 2):
            th_normal = np.pi + i * 2.0 * np.pi
            th_normal = np.array([th_normal])
            th_out = self.turner.get_norm_angle(th_in, th_normal, self.rng)
            th_outs.append(th_out[0])
        print(th_outs)
        dths = angle_dist(th_outs, th_outs[0])
        print(dths)
        self.assertTrue(np.allclose(dths, 0.0))


class TestBounceBackTurner(TestTurner):
    turner_cls = turners.BounceBackTurner

    def test_right_left(self):
        self.do_turning(self.left, self.right, self.left)

    def test_up_left(self):
        self.do_turning(self.left, self.up, self.down)

    def test_down_left(self):
        self.do_turning(self.left, self.down, self.up)


class TestReflectTurner(TestTurner):
    turner_cls = turners.ReflectTurner

    def test_right_left(self):
        self.do_turning(self.left, self.right, self.left)

    def test_up_left(self):
        self.do_turning(self.left, self.up, self.up)

    def test_down_left(self):
        self.do_turning(self.left, self.down, self.down)

    def test_left_right(self):
        self.do_turning(self.right, self.left, self.right)

    def test_up_right(self):
        self.do_turning(self.right, self.up, self.up)

    def test_down_right(self):
        self.do_turning(self.right, self.down, self.down)

    def test_right_up(self):
        self.do_turning(self.up, self.right, self.right)

    def test_left_up(self):
        self.do_turning(self.up, self.left, self.left)

    def test_down_up(self):
        self.do_turning(self.up, self.down, self.up)

    def test_right_down(self):
        self.do_turning(self.down, self.right, self.right)

    def test_left_down(self):
        self.do_turning(self.down, self.left, self.left)

    def test_up_down(self):
        self.do_turning(self.down, self.up, self.down)


class TestAlignTurner(TestTurner):
    turner_cls = turners.AlignTurner

    def test_up_left(self):
        self.do_turning(self.left, self.up, self.up)

    def test_down_left(self):
        self.do_turning(self.left, self.down, self.down)

    def test_up_right(self):
        self.do_turning(self.right, self.up, self.up)

    def test_down_right(self):
        self.do_turning(self.right, self.down, self.down)

    def test_right_up(self):
        self.do_turning(self.up, self.right, self.right)

    def test_left_up(self):
        self.do_turning(self.up, self.left, self.left)

    def test_right_down(self):
        self.do_turning(self.down, self.right, self.right)

    def test_left_down(self):
        self.do_turning(self.down, self.left, self.left)

    def test_NE_left(self):
        self.do_turning(self.left, self.NE, self.up)

    def test_SE_left(self):
        self.do_turning(self.left, self.SE, self.down)

    def test_NW_right(self):
        self.do_turning(self.right, self.NW, self.up)

    def test_SW_right(self):
        self.do_turning(self.right, self.SW, self.down)

    def do_antiparallel(self, th_in, th_normal, th_out_1, th_out_2):
        self.turner = self.turner_cls()
        n = 1000
        th_in = np.full([n], th_in)
        th_normal = np.full([n], th_normal)

        th_out = self.turner.get_norm_angle(th_in, th_normal, self.rng)
        print(th_out)

        frac_1 = np.isclose(angle_dist(th_out, th_out_1), 0.0).sum() / float(n)
        self.assertAlmostEqual(frac_1, 0.5, 1)
        frac_2 = np.isclose(angle_dist(th_out, th_out_2), 0.0).sum() / float(n)
        self.assertAlmostEqual(frac_2, 0.5, 1)

    def test_right_left(self):
        self.do_antiparallel(self.right, self.left, self.up, self.down)

    def test_down_up(self):
        self.do_antiparallel(self.down, self.up, self.left, self.right)

    def test_NE_SW(self):
        self.do_antiparallel(self.NE, self.SW, self.NW, self.SE)
