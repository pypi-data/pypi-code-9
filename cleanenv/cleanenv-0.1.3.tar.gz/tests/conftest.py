import argparse

import py.path
import pytest


@pytest.fixture(scope='session')
def datadir():
    here = py.path.local(__file__).dirpath()
    return here.join('data')


@pytest.fixture(scope='function')
def parser():
    return argparse.ArgumentParser()


@pytest.fixture(scope='function')
def environ():
    return {}

