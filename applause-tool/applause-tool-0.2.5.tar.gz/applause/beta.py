from .product import ApplauseProduct
from . import settings


class ApplauseBETA(ApplauseProduct):
    """
    Applause MBM API wrapper
    """
    BASE_URL = settings.MBM_BASE_URL
    INSTALLER_STORE_URL = settings.MBM_INSTALLER_STORE_URL
    DISTRIBUTE_URL = settings.MBM_DISTRIBUTE_URL

    def distribute(self, company_id, app_id, path, changelog=None, emails=None):
        raise NotImplementedError