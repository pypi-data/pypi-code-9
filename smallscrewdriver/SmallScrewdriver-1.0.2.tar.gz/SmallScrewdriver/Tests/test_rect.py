# encoding: utf8
from unittest import TestCase, expectedFailure
from SmallScrewdriver import Rect, Size, Point


class TestRect(TestCase):
    def test_area(self):
        r = Rect(Point(0, 0), Size(10, 10))
        self.assertEqual(r.area(), 100)

        r = Rect(Point(10, 10), Size(20, 20))
        self.assertEqual(r.area(), 400)

        r = Rect(Point(20, 20), Size(50, 50))
        self.assertEqual(r.area(), 2500)

        r = Rect(Point(100, 100), Size(200, 300))
        self.assertEqual(r.area(), 60000)

    def test_eq(self):
        r1 = Rect(Point(0, 0), Size(10, 10))
        r2 = Rect(Point(10, 10), Size(20, 20))
        r3 = Rect(Point(20, 20), Size(50, 50))
        r4 = Rect(Point(100, 100), Size(200, 300))
        r5 = Rect(Point(0, 0), Size(10, 10))

        self.assertEqual(r1, r5)
        self.assertNotEqual(r1, r2)
        self.assertNotEqual(r1, r3)
        self.assertNotEqual(r1, r4)

        self.assertNotEqual(r2, r3)
        self.assertNotEqual(r2, r4)
        self.assertNotEqual(r2, r5)

        self.assertNotEqual(r3, r4)
        self.assertNotEqual(r3, r5)

        self.assertNotEqual(r4, r5)

    def test_split_sas(self):
        r1 = Rect(Point(10, 10), Size(512, 512))
        r2 = Rect(Point(), Size(110, 75))
        r3 = Rect(Point(), Size(70, 95))
        r4 = Rect(Point(), Size(90, 55))
        r5 = Rect(Point(), Size(50, 75))

        r6 = Rect(Point(), Size(110, 50))
        r7 = Rect(Point(), Size(70, 75))

        # Плохие примеры
        r8 = Rect(Point(), Size(512, 512))
        s, rs1_, rs2_, r = r1.split(r8, Rect.RULE_SAS)
        self.assertEqual(s, 0)
        self.assertEqual(rs1_, Rect())
        self.assertEqual(rs2_, Rect())
        self.assertEqual(r, False)

        r9 = Rect(Point(), Size(200, 70))
        s, rs1_, rs2_, r = r2.split(r9, Rect.RULE_SAS)
        self.assertEqual(s, 0)
        self.assertEqual(rs1_, Rect())
        self.assertEqual(rs2_, Rect())
        self.assertEqual(r, False)

        r10 = Rect(Point(), Size(50, 80))
        s, rs1_, rs2_, r = r2.split(r10, Rect.RULE_SAS)
        self.assertEqual(s, 2)
        self.assertEqual(rs1_, Rect(r2.origin + Point(r10.size.height, 0),
                                    Size(r2.size.width - r10.size.height, r2.size.height)))
        self.assertEqual(rs2_, Rect(r2.origin + Point(0, r10.size.width),
                                    Size(r10.size.height, r2.size.height - r10.size.width)))
        self.assertEqual(r, True)

        # 1
        s, ro1, ro2, r = r2.split(r6, Rect.RULE_SAS)
        self.assertEqual(s, 1)
        self.assertEqual(ro1, Rect(Point(r2.origin.x,
                                         r2.origin.y + r6.size.height),
                                   Size(r2.size.width,
                                        r2.size.height - r6.size.height)))
        self.assertEqual(ro2, Rect())

        s, ro1, ro2, r = r2.split(r7, Rect.RULE_SAS)
        self.assertEqual(s, 1)
        self.assertEqual(ro1, Rect(Point(r2.origin.x + r7.size.width,
                                         r2.origin.y),
                                   Size(r2.size.width - r7.size.width,
                                        r2.size.height)))
        self.assertEqual(ro2, Rect())

        # test SAS
        s, rs1, rs2, r = r1.split(r2, Rect.RULE_SAS)
        self.assertEqual(s, 2)
        self.assertEqual(rs1, Rect(Point(r1.origin.x + r2.size.width,
                                         r1.origin.y),
                                   Size(r1.size.width - r2.size.width,
                                        r1.size.height)))

        self.assertEqual(rs2, Rect(Point(r1.origin.x,
                                         r1.origin.y + r2.size.height),
                                   Size(r2.size.width,
                                        r1.size.height - r2.size.height)))

        s, rs3, rs4, r = rs1.split(r3, Rect.RULE_SAS)
        self.assertEqual(s, 2)
        self.assertEqual(rs3, Rect(Point(rs1.origin.x + r3.size.width,
                                         rs1.origin.y),
                                   Size(rs1.size.width - r3.size.width,
                                        r3.size.height)))

        self.assertEqual(rs4, Rect(Point(rs1.origin.x,
                                         rs1.origin.y + r3.size.height),
                                   Size(rs1.size.width,
                                        rs1.size.height - r3.size.height)))

        s, rs5, rs6, r = rs3.split(r4, Rect.RULE_SAS)
        self.assertEqual(s, 2)
        self.assertEqual(rs5, Rect(Point(rs3.origin.x + r4.size.width,
                                         rs3.origin.y),
                                   Size(rs3.size.width - r4.size.width,
                                        rs3.size.height)))

        self.assertEqual(rs6, Rect(Point(rs3.origin.x,
                                         rs3.origin.y + r4.size.height),
                                   Size(r4.size.width,
                                        rs3.size.height - r4.size.height)))

        # test LAS

    def test_split_las(self):
        r1 = Rect(Point(10, 10), Size(512, 512))
        r2 = Rect(Point(), Size(110, 75))
        r3 = Rect(Point(), Size(70, 95))
        r4 = Rect(Point(), Size(90, 55))

        s, rs1, rs2, r = r1.split(r2, Rect.RULE_LAS)
        self.assertEqual(s, 2)
        self.assertEqual(rs1, Rect(r1.origin + Point(r2.size.width, 0),
                                   Size(r1.size.width - r2.size.width, r2.size.height)))
        self.assertEqual(rs2, Rect(r1.origin + Point(0, r2.size.height),
                                   Size(r1.size.width, r1.size.height - r2.size.height)))
        self.assertEqual(r, False)

        s, rs3, rs4, r = rs1.split(r3, Rect.RULE_LAS)
        self.assertEqual(s, 2)
        self.assertEqual(rs3, Rect(rs1.origin + Point(r3.size.height, 0),
                                   Size(rs1.size.width - r3.size.height, r3.size.width)))
        self.assertEqual(rs4, Rect(rs1.origin + Point(0, r3.size.width),
                                   Size(rs1.size.width, rs1.size.height - r3.size.width)))
        self.assertEqual(r, True)

        s, rs5, rs6, r = rs3.split(r4, Rect.RULE_LAS)
        self.assertEqual(s, 2)
        self.assertEqual(rs5, Rect(rs3.origin + Point(r4.size.width, 0),
                                   Size(rs3.size.width - r4.size.width, r4.size.height)))
        self.assertEqual(rs6, Rect(rs3.origin + Point(0, r4.size.height),
                                   Size(rs3.size.width, rs3.size.height - r4.size.height)))
        self.assertEqual(r, False)

    def test_split_slas(self):
        r1 = Rect(Point(10, 10), Size(512, 512))
        r2 = Rect(Point(), Size(110, 75))
        r3 = Rect(Point(), Size(70, 95))
        r4 = Rect(Point(), Size(90, 55))

        s, rs1, rs2, r = r1.split(r2, Rect.RULE_SLAS)
        self.assertEqual(s, 2)
        self.assertEqual(rs1, Rect(r1.origin + Point(r2.size.width, 0),
                                   Size(r1.size.width - r2.size.width, r2.size.height)))
        self.assertEqual(rs2, Rect(r1.origin + Point(0, r2.size.height),
                                   Size(r1.size.width, r1.size.height - r2.size.height)))
        self.assertEqual(r, False)

        s, rs3, rs4, r = rs1.split(r3, Rect.RULE_SLAS)
        self.assertEqual(s, 2)
        self.assertEqual(rs3, Rect(rs1.origin + Point(r3.size.height, 0),
                                   Size(rs1.size.width - r3.size.height, rs1.size.height)))
        self.assertEqual(rs4, Rect(rs1.origin + Point(0, r3.size.width),
                                   Size(r3.size.height, rs1.size.height - r3.size.width)))
        self.assertEqual(r, True)

        s, rs5, rs6, r = rs3.split(r4, Rect.RULE_SLAS)
        self.assertEqual(s, 2)
        self.assertEqual(rs5, Rect(rs3.origin + Point(r4.size.width, 0),
                                   Size(rs3.size.width - r4.size.width, rs3.size.height)))
        self.assertEqual(rs6, Rect(rs3.origin + Point(0, r4.size.height),
                                   Size(r4.size.width, rs3.size.height - r4.size.height)))
        self.assertEqual(r, False)

    def test_split_llas(self):
        r1 = Rect(Point(10, 10), Size(512, 512))
        r2 = Rect(Point(), Size(110, 75))
        r3 = Rect(Point(), Size(70, 95))
        r4 = Rect(Point(), Size(90, 55))

        # Вертикально
        s, rs1, rs2, r = r1.split(r2, Rect.RULE_LLAS)
        self.assertEqual(s, 2)
        self.assertEqual(rs1, Rect(r1.origin + Point(r2.size.width, 0),
                                   Size(r1.size.width - r2.size.width, r1.size.height)))
        self.assertEqual(rs2, Rect(r1.origin + Point(0, r2.size.height),
                                   Size(r2.size.width, r1.size.height - r2.size.height)))
        self.assertEqual(r, False)

        # Вертикально
        s, rs3, rs4, r = rs1.split(r3, Rect.RULE_LLAS)
        self.assertEqual(s, 2)
        self.assertEqual(rs3, Rect(rs1.origin + Point(r3.size.width, 0),
                                   Size(rs1.size.width - r3.size.width, rs1.size.height)))
        self.assertEqual(rs4, Rect(rs1.origin + Point(0, r3.size.height),
                                   Size(r3.size.width, rs1.size.height - r3.size.height)))
        self.assertEqual(r, False)

        s, rs5, rs6, r = rs3.split(r4, Rect.RULE_LLAS)
        self.assertEqual(s, 2)
        self.assertEqual(rs5, Rect(rs3.origin + Point(r4.size.width, 0),
                                   Size(rs3.size.width - r4.size.width, rs3.size.height)))
        self.assertEqual(rs6, Rect(rs3.origin + Point(0, r4.size.height),
                                   Size(r4.size.width, rs3.size.height - r4.size.height)))
        self.assertEqual(r, False)

    def test_split_pick_both(self):
        r1 = Rect(Point(10, 10), Size(512, 512))
        r2 = Rect(Point(), Size(110, 75))
        r3 = Rect(Point(), Size(70, 95))
        r4 = Rect(Point(), Size(90, 55))

        s, rs1, rs2, r = r1.split(r2, Rect.RULE_PICK_BOTH)
        self.assertEqual(s, 2)
        self.assertEqual(rs1, Rect(r1.origin + Point(r2.size.width, 0),
                                   Size(r1.size.width - r2.size.width, r1.size.height)))
        self.assertEqual(rs2, Rect(r1.origin + Point(0, r2.size.height),
                                   Size(r1.size.width, r1.size.height - r2.size.height)))
        self.assertEqual(r, False)

        s, rs3, rs4, r = rs1.split(r3, Rect.RULE_PICK_BOTH)
        self.assertEqual(s, 2)
        self.assertEqual(rs3, Rect(rs1.origin + Point(r3.size.width, 0),
                                   Size(rs1.size.width - r3.size.width, rs1.size.height)))
        self.assertEqual(rs4, Rect(rs1.origin + Point(0, r3.size.height),
                                   Size(rs1.size.width, rs1.size.height - r3.size.height)))
        self.assertEqual(r, False)

        s, rs5, rs6, r = rs3.split(r4, Rect.RULE_PICK_BOTH)
        self.assertEqual(s, 2)
        self.assertEqual(rs5, Rect(rs3.origin + Point(r4.size.width, 0),
                                   Size(rs3.size.width - r4.size.width, rs3.size.height)))
        self.assertEqual(rs6, Rect(rs3.origin + Point(0, r4.size.height),
                                   Size(rs3.size.width, rs3.size.height - r4.size.height)))
        self.assertEqual(r, False)

    def test_intersection(self):

        r1 = Rect(Point(10, 10), Size(30, 30))
        r2 = Rect(Point(20, 20), Size(10, 10))

        r = r1.intersection(r2)
        self.assertEqual(r, r2)

        r3 = Rect(Point(10, 10), Size(20, 40))
        r4 = Rect(Point(15, 15), Size(15, 15))

        r = r3.intersection(r4)
        self.assertEqual(r, Rect(Point(15, 15), Size(15, 15)))

        r5 = Rect(Point(4, 4), Size(8, 8))
        r6 = Rect(Point(9, 9), Size(12, 12))

        r = r5.intersection(r6)
        self.assertEqual(r, Rect(Point(9, 9), Size(3, 3)))

        r7 = Rect(Point(5, 5), Size(5, 5))
        r8 = Rect(Point(5, 10), Size(10, 10))

        r = r7.intersection(r8)
        self.assertEqual(r, Rect(Point(5, 10), Size(5, 0)))
