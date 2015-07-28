# -*- coding: utf-8 -*-
import re
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

COUNTRIES = (
    ("US", _(u"United States")),
    ("CA", _(u"Canada")),
    ("MX", _(u"Mexico")),
    ("AF", _(u"Afghanistan")),
    ("AX", _(u"Åland Islands")),
    ("AL", _(u"Albania")),
    ("DZ", _(u"Algeria")),
    ("AS", _(u"American Samoa")),
    ("AD", _(u"Andorra")),
    ("AO", _(u"Angola")),
    ("AI", _(u"Anguilla")),
    ("AQ", _(u"Antarctica")),
    ("AG", _(u"Antigua and Barbuda")),
    ("AR", _(u"Argentina")),
    ("AM", _(u"Armenia")),
    ("AW", _(u"Aruba")),
    ("AU", _(u"Australia")),
    ("AT", _(u"Austria")),
    ("AZ", _(u"Azerbaijan")),
    ("BS", _(u"Bahamas")),
    ("BH", _(u"Bahrain")),
    ("BD", _(u"Bangladesh")),
    ("BB", _(u"Barbados")),
    ("BY", _(u"Belarus")),
    ("BE", _(u"Belgium")),
    ("BZ", _(u"Belize")),
    ("BJ", _(u"Benin")),
    ("BM", _(u"Bermuda")),
    ("BT", _(u"Bhutan")),
    ("BO", _(u"Bolivia, Plurinational State of")),
    ("BQ", _(u"Bonaire, Sint Eustatius and Saba")),
    ("BA", _(u"Bosnia and Herzegovina")),
    ("BW", _(u"Botswana")),
    ("BV", _(u"Bouvet Island")),
    ("BR", _(u"Brazil")),
    ("IO", _(u"British Indian Ocean Territory")),
    ("BN", _(u"Brunei Darussalam")),
    ("BG", _(u"Bulgaria")),
    ("BF", _(u"Burkina Faso")),
    ("BI", _(u"Burundi")),
    ("KH", _(u"Cambodia")),
    ("CM", _(u"Cameroon")),
    ("CV", _(u"Cape Verde")),
    ("KY", _(u"Cayman Islands")),
    ("CF", _(u"Central African Republic")),
    ("TD", _(u"Chad")),
    ("CL", _(u"Chile")),
    ("CN", _(u"China")),
    ("CX", _(u"Christmas Island")),
    ("CC", _(u"Cocos (Keeling) Islands")),
    ("CO", _(u"Colombia")),
    ("KM", _(u"Comoros")),
    ("CG", _(u"Congo")),
    ("CD", _(u"Congo (the Democratic Republic of the)")),
    ("CK", _(u"Cook Islands")),
    ("CR", _(u"Costa Rica")),
    ("CI", _(u"Côte d'Ivoire")),
    ("HR", _(u"Croatia")),
    ("CU", _(u"Cuba")),
    ("CW", _(u"Curaçao")),
    ("CY", _(u"Cyprus")),
    ("CZ", _(u"Czech Republic")),
    ("DK", _(u"Denmark")),
    ("DJ", _(u"Djibouti")),
    ("DM", _(u"Dominica")),
    ("DO", _(u"Dominican Republic")),
    ("EC", _(u"Ecuador")),
    ("EG", _(u"Egypt")),
    ("SV", _(u"El Salvador")),
    ("GQ", _(u"Equatorial Guinea")),
    ("ER", _(u"Eritrea")),
    ("EE", _(u"Estonia")),
    ("ET", _(u"Ethiopia")),
    ("FK", _(u"Falkland Islands  [Malvinas]")),
    ("FO", _(u"Faroe Islands")),
    ("FJ", _(u"Fiji")),
    ("FI", _(u"Finland")),
    ("FR", _(u"France")),
    ("GF", _(u"French Guiana")),
    ("PF", _(u"French Polynesia")),
    ("TF", _(u"French Southern Territories")),
    ("GA", _(u"Gabon")),
    ("GM", _(u"Gambia (The)")),
    ("GE", _(u"Georgia")),
    ("DE", _(u"Germany")),
    ("GH", _(u"Ghana")),
    ("GI", _(u"Gibraltar")),
    ("GR", _(u"Greece")),
    ("GL", _(u"Greenland")),
    ("GD", _(u"Grenada")),
    ("GP", _(u"Guadeloupe")),
    ("GU", _(u"Guam")),
    ("GT", _(u"Guatemala")),
    ("GG", _(u"Guernsey")),
    ("GN", _(u"Guinea")),
    ("GW", _(u"Guinea-Bissau")),
    ("GY", _(u"Guyana")),
    ("HT", _(u"Haiti")),
    ("HM", _(u"Heard Island and McDonald Islands")),
    ("VA", _(u"Holy See  [Vatican City State]")),
    ("HN", _(u"Honduras")),
    ("HK", _(u"Hong Kong")),
    ("HU", _(u"Hungary")),
    ("IS", _(u"Iceland")),
    ("IN", _(u"India")),
    ("ID", _(u"Indonesia")),
    ("IR", _(u"Iran (the Islamic Republic of)")),
    ("IQ", _(u"Iraq")),
    ("IE", _(u"Ireland")),
    ("IM", _(u"Isle of Man")),
    ("IL", _(u"Israel")),
    ("IT", _(u"Italy")),
    ("JM", _(u"Jamaica")),
    ("JP", _(u"Japan")),
    ("JE", _(u"Jersey")),
    ("JO", _(u"Jordan")),
    ("KZ", _(u"Kazakhstan")),
    ("KE", _(u"Kenya")),
    ("KI", _(u"Kiribati")),
    ("KP", _(u"Korea (the Democratic People's Republic of)")),
    ("KR", _(u"Korea (the Republic of)")),
    ("XK", _(u"Kosovo (Republic of)")),
    ("KW", _(u"Kuwait")),
    ("KG", _(u"Kyrgyzstan")),
    ("LA", _(u"Lao People's Democratic Republic")),
    ("LV", _(u"Latvia")),
    ("LB", _(u"Lebanon")),
    ("LS", _(u"Lesotho")),
    ("LR", _(u"Liberia")),
    ("LY", _(u"Libya")),
    ("LI", _(u"Liechtenstein")),
    ("LT", _(u"Lithuania")),
    ("LU", _(u"Luxembourg")),
    ("MO", _(u"Macao")),
    ("MK", _(u"Macedonia (the former Yugoslav Republic of)")),
    ("MG", _(u"Madagascar")),
    ("MW", _(u"Malawi")),
    ("MY", _(u"Malaysia")),
    ("MV", _(u"Maldives")),
    ("ML", _(u"Mali")),
    ("MT", _(u"Malta")),
    ("MH", _(u"Marshall Islands")),
    ("MQ", _(u"Martinique")),
    ("MR", _(u"Mauritania")),
    ("MU", _(u"Mauritius")),
    ("YT", _(u"Mayotte")),
    ("FM", _(u"Micronesia (the Federated States of)")),
    ("MD", _(u"Moldova (the Republic of)")),
    ("MC", _(u"Monaco")),
    ("MN", _(u"Mongolia")),
    ("ME", _(u"Montenegro")),
    ("MS", _(u"Montserrat")),
    ("MA", _(u"Morocco")),
    ("MZ", _(u"Mozambique")),
    ("MM", _(u"Myanmar")),
    ("NA", _(u"Namibia")),
    ("NR", _(u"Nauru")),
    ("NP", _(u"Nepal")),
    ("NL", _(u"Netherlands")),
    ("NC", _(u"New Caledonia")),
    ("NZ", _(u"New Zealand")),
    ("NI", _(u"Nicaragua")),
    ("NE", _(u"Niger")),
    ("NG", _(u"Nigeria")),
    ("NU", _(u"Niue")),
    ("NF", _(u"Norfolk Island")),
    ("MP", _(u"Northern Mariana Islands")),
    ("NO", _(u"Norway")),
    ("OM", _(u"Oman")),
    ("PK", _(u"Pakistan")),
    ("PW", _(u"Palau")),
    ("PS", _(u"Palestine, State of")),
    ("PA", _(u"Panama")),
    ("PG", _(u"Papua New Guinea")),
    ("PY", _(u"Paraguay")),
    ("PE", _(u"Peru")),
    ("PH", _(u"Philippines")),
    ("PN", _(u"Pitcairn")),
    ("PL", _(u"Poland")),
    ("PT", _(u"Portugal")),
    ("PR", _(u"Puerto Rico")),
    ("QA", _(u"Qatar")),
    ("RE", _(u"Réunion")),
    ("RO", _(u"Romania")),
    ("RU", _(u"Russian Federation")),
    ("RW", _(u"Rwanda")),
    ("BL", _(u"Saint Barthélemy")),
    ("SH", _(u"Saint Helena, Ascension and Tristan da Cunha")),
    ("KN", _(u"Saint Kitts and Nevis")),
    ("LC", _(u"Saint Lucia")),
    ("MF", _(u"Saint Martin (French part)")),
    ("PM", _(u"Saint Pierre and Miquelon")),
    ("VC", _(u"Saint Vincent and the Grenadines")),
    ("WS", _(u"Samoa")),
    ("SM", _(u"San Marino")),
    ("ST", _(u"Sao Tome and Principe")),
    ("SA", _(u"Saudi Arabia")),
    ("SN", _(u"Senegal")),
    ("RS", _(u"Serbia")),
    ("SC", _(u"Seychelles")),
    ("SL", _(u"Sierra Leone")),
    ("SG", _(u"Singapore")),
    ("SX", _(u"Sint Maarten (Dutch part)")),
    ("SK", _(u"Slovakia")),
    ("SI", _(u"Slovenia")),
    ("SB", _(u"Solomon Islands")),
    ("SO", _(u"Somalia")),
    ("ZA", _(u"South Africa")),
    ("GS", _(u"South Georgia and the South Sandwich Islands")),
    ("SS", _(u"South Sudan")),
    ("ES", _(u"Spain")),
    ("LK", _(u"Sri Lanka")),
    ("SD", _(u"Sudan")),
    ("SR", _(u"Suriname")),
    ("SJ", _(u"Svalbard and Jan Mayen")),
    ("SZ", _(u"Swaziland")),
    ("SE", _(u"Sweden")),
    ("CH", _(u"Switzerland")),
    ("SY", _(u"Syrian Arab Republic")),
    ("TW", _(u"Taiwan (Province of China)")),
    ("TJ", _(u"Tajikistan")),
    ("TZ", _(u"Tanzania, United Republic of")),
    ("TH", _(u"Thailand")),
    ("TL", _(u"Timor-Leste")),
    ("TG", _(u"Togo")),
    ("TK", _(u"Tokelau")),
    ("TO", _(u"Tonga")),
    ("TT", _(u"Trinidad and Tobago")),
    ("TN", _(u"Tunisia")),
    ("TR", _(u"Turkey")),
    ("TM", _(u"Turkmenistan")),
    ("TC", _(u"Turks and Caicos Islands")),
    ("TV", _(u"Tuvalu")),
    ("UG", _(u"Uganda")),
    ("UA", _(u"Ukraine")),
    ("AE", _(u"United Arab Emirates")),
    ("GB", _(u"United Kingdom")),
    ("UM", _(u"United States Minor Outlying Islands")),
    ("UY", _(u"Uruguay")),
    ("UZ", _(u"Uzbekistan")),
    ("VU", _(u"Vanuatu")),
    ("VE", _(u"Venezuela, Bolivarian Republic of")),
    ("VN", _(u"Viet Nam")),
    ("VG", _(u"Virgin Islands (British)")),
    ("VI", _(u"Virgin Islands (U.S.)")),
    ("WF", _(u"Wallis and Futuna")),
    ("EH", _(u"Western Sahara")),
    ("YE", _(u"Yemen")),
    ("ZM", _(u"Zambia")),
    ("ZW", _(u"Zimbabwe"))
)

    

#: All 50 states, plus the District of Columbia.
US_STATES = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('DC', 'District of Columbia'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
)

#: Non-state territories.
US_TERRITORIES = (
    ('AS', 'American Samoa'),
    ('GU', 'Guam'),
    ('MP', 'Northern Mariana Islands'),
    ('PR', 'Puerto Rico'),
    ('VI', 'Virgin Islands'),
)

#: Military postal "states". Note that 'AE' actually encompasses
#: Europe, Canada, Africa and the Middle East.
ARMED_FORCES_STATES = (
    ('AA', 'Armed Forces Americas'),
    ('AE', 'Armed Forces Europe'),
    ('AP', 'Armed Forces Pacific'),
)

#: Non-US locations serviced by USPS (under Compact of Free
#: Association).
COFA_STATES = (
    ('FM', 'Federated States of Micronesia'),
    ('MH', 'Marshall Islands'),
    ('PW', 'Palau'),
)

#: Obsolete abbreviations (no longer US territories/USPS service, or
#: code changed).
OBSOLETE_STATES = (
    ('CM', 'Commonwealth of the Northern Mariana Islands'),  # Is now 'MP'
    ('CZ', 'Panama Canal Zone'),                             # Reverted to Panama 1979
    ('PI', 'Philippine Islands'),                            # Philippine independence 1946
    ('TT', 'Trust Territory of the Pacific Islands'),        # Became the independent COFA states + Northern Mariana Islands 1979-1994
)


#: All US states and territories plus DC and military mail.
STATE_CHOICES = tuple(sorted(US_STATES + US_TERRITORIES + ARMED_FORCES_STATES, key=lambda obj: obj[1]))

#: All US Postal Service locations.
USPS_CHOICES = tuple(sorted(US_STATES + US_TERRITORIES + ARMED_FORCES_STATES + COFA_STATES, key=lambda obj: obj[1]))

def unique_slugify(instance, value, slug_field_name='slug', queryset=None,
                   slug_separator='-'):
    """
    Calculates and stores a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '%s%s' % (slug_separator, next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len-len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        next += 1

    setattr(instance, slug_field.attname, slug)


def _slug_strip(value, separator='-'):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    """
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
    # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
    # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
    return value