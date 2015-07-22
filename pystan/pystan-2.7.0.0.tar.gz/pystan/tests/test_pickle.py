import os
import pickle
import sys
import tempfile
import unittest

import pystan


class TestPickle(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tmpdir = tmpdir = tempfile.mkdtemp()
        cls.pickle_file = os.path.join(tmpdir, 'stanmodel.pkl')
        cls.model_code = 'parameters {real y;} model {y ~ normal(0,1);}'

    def test_pickle_model_no_save_dso(self):
        pickle_file = self.pickle_file
        model_code = self.model_code
        m = pystan.StanModel(model_code=model_code, model_name="normal1",
                             save_dso=False)
        module_name = m.module.__name__
        with open(pickle_file, 'wb') as f:
            pickle.dump(m, f)
        del m
        del sys.modules[module_name]

        with open(pickle_file, 'rb') as f:
            m = pickle.load(f)
        self.assertTrue(m.model_name.startswith("normal1"))

    def test_pickle_model(self):
        pickle_file = self.pickle_file
        model_code = self.model_code
        m = pystan.StanModel(model_code=model_code, model_name="normal2")
        module_name = m.module.__name__
        module_filename = m.module.__file__
        with open(pickle_file, 'wb') as f:
            pickle.dump(m, f)
        del m
        del sys.modules[module_name]

        with open(pickle_file, 'rb') as f:
            m = pickle.load(f)
        self.assertTrue(m.model_name.startswith("normal2"))
        self.assertIsNotNone(m.module)
        self.assertNotEqual(module_filename, m.module.__file__)
        fit = m.sampling()
        y = fit.extract()['y']
        assert len(y) == 4000

    def test_pickle_fit(self):
        tmpdir = self.tmpdir
        num_iter = 100
        fit_pickle_filename = os.path.join(tmpdir, 'stanfit.pkl')
        model_pickle_filename = os.path.join(tmpdir, 'stanmodel.pkl')
        model_code = 'parameters {real y;} model {y ~ normal(0,1);}'

        sm = pystan.StanModel(model_code=model_code, model_name="normal1")

        # additional error checking
        fit = sm.sampling(iter=num_iter)
        y = fit.extract()['y'].copy()
        self.assertIsNotNone(y)

        # pickle
        with open(model_pickle_filename, 'wb') as f:
            pickle.dump(sm, f)

        with open(fit_pickle_filename, 'wb') as f:
            pickle.dump(fit, f)
        del fit

        # unload module
        module_name = sm.module.__name__
        if module_name in sys.modules:
            del(sys.modules[module_name])

        # load from file
        with open(model_pickle_filename, 'rb') as f:
            sm_from_pickle = pickle.load(f)  # noqa
        with open(fit_pickle_filename, 'rb') as f:
            fit_from_pickle = pickle.load(f)

        self.assertIsNotNone(fit_from_pickle)
        self.assertTrue((fit_from_pickle.extract()['y'] == y).all())
