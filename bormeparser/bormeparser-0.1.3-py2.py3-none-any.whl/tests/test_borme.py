#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# test_borme.py -
# Copyright (C) 2015 Pablo Castellano <pablo@anche.no>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import unittest

from bormeparser.borme import Borme, BormeActoCargo, BormeActoTexto, BormeAnuncio
from bormeparser.seccion import SECCION
from bormeparser.provincia import PROVINCIA


# TODO: Añadir un BormeActoTexto
DATA1 = {214028: {'Actos': {'Ceses/Dimisiones': {'Adm. Unico': {'JUAN GARCIA GARCIA'}},
                            'Datos registrales': 'T 5188, L 4095, F 146, S 8, H MA120039, I/A 4 (25.05.15).',
                            'Nombramientos': {'Adm. Unico': {'PEDRO GOMEZ GOMEZ'}}},
                  'Empresa': 'EMPRESA RANDOM SL.'},
         'borme_cve': 'BORME-A-2015-102-29',
         'borme_fecha': 'Martes 2 de junio de 2015',
         'borme_num': 102,
         'borme_provincia': 'MÁLAGA',
         'borme_seccion': 'SECCIÓN PRIMERA'
         }


class BormeTestCase(unittest.TestCase):

    def test_borme_instance(self):
        bormeanuncios = []
        a = BormeAnuncio(1, DATA1[214028]['Empresa'], DATA1[214028]['Actos'])
        bormeanuncios.append(a)

        fecha = (2015, 2, 10)
        borme = Borme(fecha, 'A', PROVINCIA.CACERES, 27, 'BORME-A-2015-27-10', bormeanuncios)
        self.assertEqual(borme.date, datetime.date(year=2015, month=2, day=10))
        self.assertEqual(borme.seccion, SECCION.A)
        self.assertEqual(borme.provincia, PROVINCIA.CACERES)
        self.assertEqual(borme.num, 27)
        self.assertEqual(borme.cve, 'BORME-A-2015-27-10')
        self.assertEqual(borme.url, 'http://boe.es/borme/dias/2015/02/10/pdfs/BORME-A-2015-27-10.pdf')
        self.assertEqual(borme.filename, None)

    def test_bormeanuncio_instance(self):
        anuncio = BormeAnuncio(1, DATA1[214028]['Empresa'], DATA1[214028]['Actos'])
        self.assertEqual(anuncio.id, 1)
        self.assertEqual(anuncio.empresa, DATA1[214028]['Empresa'])
        self.assertEqual(anuncio.datos_registrales, DATA1[214028]['Actos']['Datos registrales'])

        actos = list(anuncio.get_actos())
        actos.sort()
        self.assertEqual(len(actos), 2)
        # FIXME: orden 0 y 1
        self.assertEqual(actos[0], ('Ceses/Dimisiones', DATA1[214028]['Actos']['Ceses/Dimisiones']))
        self.assertEqual(actos[1], ('Nombramientos', DATA1[214028]['Actos']['Nombramientos']))

        actos = anuncio.get_borme_actos()
        actos.sort()
        self.assertEqual(len(actos), 2)
        self.assertIsInstance(actos[0], BormeActoCargo)
        self.assertEqual(actos[0].name, 'Ceses/Dimisiones')
        self.assertEqual(actos[0].cargos, DATA1[214028]['Actos']['Ceses/Dimisiones'])
        self.assertIsInstance(actos[1], BormeActoCargo)
        self.assertEqual(actos[1].name, 'Nombramientos')
        self.assertEqual(actos[1].cargos, DATA1[214028]['Actos']['Nombramientos'])

    def test_bormeactocargo_instance(self):
        self.assertRaises(ValueError, BormeActoCargo, 'Acto invalido', 'mal')
        self.assertRaises(ValueError, BormeActoCargo, 'Constitución', 'mal')
        self.assertRaises(ValueError, BormeActoCargo, 'Nombramientos', 'mal')
        acto = BormeActoCargo('Nombramientos', DATA1[214028]['Actos']['Nombramientos'])
        self.assertEqual(len(acto.cargos), 1)
        self.assertEqual(acto.cargos['Adm. Unico'], DATA1[214028]['Actos']['Nombramientos']['Adm. Unico'])

    def test_bormeactotexto_instance(self):
        self.assertRaises(ValueError, BormeActoTexto, 'Acto invalido', ['mal'])
        self.assertRaises(ValueError, BormeActoTexto, 'Nombramientos', ['mal'])
        acto = BormeActoTexto('Constitución', 'Constitución de la empresa')
        self.assertEqual(acto.value, 'Constitución de la empresa')


if __name__ == '__main__':
    unittest.main()
