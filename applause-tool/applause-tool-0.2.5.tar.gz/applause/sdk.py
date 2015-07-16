from .product import ApplauseProduct
from . import settings


class ApplauseSDK(ApplauseProduct):
    """
    Applause SDK API wrapper
    """
    BASE_URL = settings.SDK_BASE_URL
    INSTALLER_STORE_URL = settings.SDK_INSTALLER_STORE_URL
    DISTRIBUTE_URL = settings.SDK_DISTRIBUTE_URL