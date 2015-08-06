import pyhacrf
from pyhacrf.pyhacrf import Hacrf
from pyhacrf.features import StringPairFeatureExtractor

import numpy


class CRFEditDistance(object) :
    def __init__(self) :
        self.model = Hacrf(l2_regularization=1.0)
        model.parameters = numpy.array([[ 0.15467246, -0.24446651],
                                        [ 0.44298456,  0.24446651],
                                        [-0.13156489, -0.03677116],
                                        [ 0.34085787,  0.07327131],
                                        [ 0.14636932, -0.07016704],
                                        [-0.0793364,   0.07172034],
                                        [ 0.571312,   -0.13752831],
                                        [-0.24998087,  0.09947487]])

        self.feature_extractor = StringPairFeatureExtractor(match=True,
                                                            numeric=True)

    def train(self, examples, labels) :
        extracted_examples = feature_extractor.fit_transform(examples)
        model.fit(extracted_example, labels)

    def __call__(self, string_1, string_2) :
        features = self.feature_extractor((string_1, string_2),))
        return self.model.predict(features)[0:0]
