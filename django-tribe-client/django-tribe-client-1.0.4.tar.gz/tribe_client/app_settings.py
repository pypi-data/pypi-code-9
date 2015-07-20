from django.conf import settings

TRIBE_URL = getattr(settings, 'TRIBE_URL', 'http://tribe.greenelab.com')

ACCESS_CODE_URL = TRIBE_URL + "/oauth2/authorize/"
ACCESS_TOKEN_URL = TRIBE_URL + "/oauth2/token/"

ENTREZ = 'Entrez'

CROSSREF_DB = '&xrdb=' + getattr(settings, 'TRIBE_CROSSREF_DB', ENTREZ)
CROSSREF = getattr(settings, 'TRIBE_CROSSREF_DB', ENTREZ)

TRIBE_ID = getattr(settings, 'TRIBE_ID', '')
TRIBE_SECRET= getattr(settings, 'TRIBE_SECRET', '')

TRIBE_REDIRECT_URI = getattr(settings, 'TRIBE_REDIRECT_URI', '')
