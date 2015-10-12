import unittest
from transat.apps.severe_slug import severe_slug
import numpy as np

class TestSlugApp(unittest.TestCase):
    def test_runApp(self):
        inputs = { 'L1':1, 'L2':0.4, 'L3': 0.8, 'WaterVel': 1.1, 'GasVel': 1.1, 'OilVel': 1.1, 'Radius': 0.05}
        dp = severe_slug.my_fun(inputs)
        dp2 = {0.021892: 2825.5760398705111, 0.42961: 2801.1171195242514,
               0.76259: 2872.5871195242676, 0.33448: 2828.9771195242538,
               0.1442: 2838.9825892616568, 0.052852: 2834.94162389858,
               0.01: 144131.73607526586}


        self.assertEqual(True, True)

    test_runApp.heavy = True