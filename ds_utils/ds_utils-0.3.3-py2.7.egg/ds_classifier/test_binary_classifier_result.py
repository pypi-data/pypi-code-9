import unittest
import pandas as pd
from . import BinaryClassifierResult


class BinaryResultTest(unittest.TestCase):

    def setUp(self):
        df = pd.DataFrame(dict(probability=[0, .4, .6, 1], truth=[True, False, True, True]))
        self._class = BinaryClassifierResult(df)

    def test_constructor_bad_columns(self):
        def bad_columns():
            BinaryClassifierResult(pd.DataFrame(dict(stuff=[1], other=[2])))
        self.assertRaises(ValueError, bad_columns)

    def test_constructor_non_df(self):
        def non_df():
            BinaryClassifierResult(1)
        self.assertRaises(ValueError, non_df)

    def test_accuracy(self):
        accuracy = self._class.accuracy()
        self.assertEqual(0.75, accuracy)

    def test_precision(self):
        precision = self._class.precision()
        self.assertEqual(1, precision)

    def test_recall(self):
        recall = self._class.recall()
        self.assertEqual(float(2) / 3, recall)

    def test_convert(self):
        # tests that the confusion matrix is still computed correctly when given integers for truth values
        df = pd.DataFrame(dict(probability=[0, .4, .6, 1], truth=[1, 0, 0, 1]))
        bc = BinaryClassifierResult(df)
        confusion = bc.get_confusion()

        self.assertDictEqual(confusion, dict(true_pos=1, false_pos=1, true_neg=1, false_neg=1))
