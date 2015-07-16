try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

# Not so secret client credentials :>
CLIENT_ID = "SIuumK3jrALG4RAd3iIm9Quv16see1o4"
CLIENT_SECRET = "bgsdVpJiuriqQTIA"


# Applause Auth
OAUTH_BASE_URL = 'https://applause-org-prod.apigee.net'

PLATFORM_URL = 'https://my.applause.com'

# Applause Builds

BUAPS_BASE_URL = 'https://api.applause.com/builds/'
BUAPS_STORE_URL = urljoin(BUAPS_BASE_URL, 'storage/')
BUAPS_STATUS_URL = urljoin(BUAPS_BASE_URL, 'storage/{token}/status/')
BUAPS_SUCCESS_URL = urljoin(BUAPS_BASE_URL, 'handlers/success/{token}/')


# Applause SDK
# SDK_BASE_URL = 'https://api.applause.com/sdk/'
SDK_BASE_URL = 'https://applause-org-prod.apigee.net/sdk/'
SDK_INSTALLER_STORE_URL = urljoin(SDK_BASE_URL, "resources/installer/store/")
SDK_DISTRIBUTE_URL = urljoin(SDK_BASE_URL, "companies/{company_id}/applications/{app_id}/distributions/")

# Applause MBM
MBM_BASE_URL = 'https://applause-org-prod.apigee.net/mbm/'
MBM_INSTALLER_STORE_URL = urljoin(MBM_BASE_URL, "resources/installer/store/")
MBM_DISTRIBUTE_URL = urljoin(MBM_BASE_URL, "companies/{company_id}/applications/{app_id}/distributions/")