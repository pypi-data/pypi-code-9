try:
    from binary_classifier_result import BinaryClassifierResult
except ImportError as e:
    class BinaryClassifierResult:
        msg = "\nTrying to use BinaryClassifierResult, but you're missing a package." \
              "\nIf you want to use BinaryClassifierResult, go install the package below:\n"

        def __init__(self):
            print self.msg
            raise e

        def __init__(self, param):
            print self.msg
            raise e
