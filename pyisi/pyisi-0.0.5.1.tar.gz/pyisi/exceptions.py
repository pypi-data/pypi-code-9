__author__ = 'jkingsbury'


class AEC_ERROR(Exception):
    pass


class AEC_NOT_FOUND(AEC_ERROR):
    pass


class AEC_FORBIDDEN(AEC_ERROR):
    pass


class AEC_UNAUTHORIZED(AEC_ERROR):
    pass


class AEC_SYSTEM_INTERNAL_ERROR(AEC_ERROR):
    pass


class INVALID_TYPE(Exception):
    pass