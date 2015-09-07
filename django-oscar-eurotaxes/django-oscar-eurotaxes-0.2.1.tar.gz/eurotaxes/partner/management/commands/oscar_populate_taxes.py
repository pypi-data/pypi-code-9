# coding=utf-8
__copyright__ = 'Copyright 2015, Abalt'

from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from oscar.core.loading import get_model

Country = get_model('address', 'Country')
VATType = get_model('partner', 'VATType')
VATCountry = get_model('partner', 'VATCountry')

VAT_TYPES = [
    'General',
    'Reduced',
    'Super-Reduced'
]

VAT_COUNTRIES = [
    ('AT', 20, 10, 10, False),
    ('BE', 21, 12, 6, False),
    ('BG', 20, 9, 9, False),
    ('HR', 23, 10, 10, False),
    ('CY', 17, 8, 5, False),
    ('CZ', 20, 10, 10, False),
    ('DK', 25, 25, 25, False),
    ('EE', 20, 9, 9, False),
    ('ES', 21, 10, 4, True),
    ('FI', 23, 13, 9, False),
    ('FR', 19.6, 7, 2.1, False),
    ('DE', 19, 7, 7, False),
    ('GR', 23, 13, 6.5, False),
    ('HU', 27, 18, 5, False),
    ('IE', 23, 13.5, 9, False),
    ('IT', 21, 10, 4.8, False),
    ('LV', 21, 12, 12, False),
    ('LT', 21, 9, 5, False),
    ('LU', 15, 12, 12, False),
    ('MT', 18, 5, 5, False),
    ('NL', 19, 6, 6, False),
    ('PL', 23, 8, 5, False),
    ('PT', 23, 13, 6, False),
    ('RO', 24, 9, 9, False),
    ('SK', 20, 10, 10, False),
    ('SI', 20, 8.5, 8.5, False),
    ('SE', 25, 12, 6, False),
    ('GB', 20, 5, 5, False),

]


class Command(BaseCommand):
    help = "Populates the list of taxes with data."

    def handle(self, *args, **options):

        vat_types = []
        for vat_type in VAT_TYPES:
            vat_types.append(VATType.objects.create(name=vat_type, default=False))

        vat_type_default = vat_types[0]
        vat_type_default.default = True
        vat_type_default.save()

        for vat_country in VAT_COUNTRIES:
            country = Country.objects.get(iso_3166_1_a2=vat_country[0])
            for i in xrange(len(vat_types)):
                vat_type = vat_types[i]
                VATCountry.objects.create(
                    country=country,
                    vat_type=vat_type,
                    default=vat_country[len(vat_country) - 1] and vat_type == vat_type_default,
                    vat=Decimal(vat_country[i + 1])

                )

        self.stdout.write("Successfully added taxes.")
