#encoding:utf-8
from django.test import TestCase

from microsip_api.apps.cuentasxcobrar.core import CargosClientes


class CargosClientesTests(TestCase):

    def setUp(self):
        self.client.post('/login/', {'username': 'SYSDBA', 'password': '1', 'conexion_db': '1', })

    def test_obtener_cargos_de_todos_los_clientes(self):
        """
        Checa si la funcion regresa cargos de todos los clientes
        """
        cargos = CargosClientes('email', tomar_remisiones=True,)
        self.assertTrue(len(cargos) > 1)

    def test_obtener_cargos_de_un_cliente(self):
        """
        Checa si la funcion regresa cargos de un cliente espesifico
        """

        cargos = CargosClientes('email', clientes_ids=[u'3636'], tomar_remisiones=True,)
        self.assertTrue(len(cargos) == 1)

    def test_obtener_cargos_de_un_cliente_ids_enteros(self):
        """
        Checa si la funcion regresa cargos de un cliente espesifico con enteros
        """

        cargos = CargosClientes('email', clientes_ids=[3636], tomar_remisiones=True,)
        self.assertTrue(len(cargos) == 1)

    def test_cargos_con_monto_minimo_con_remissiones(self):
        """
        no deberia de dar cargos cuando el limite es 999999999
        """
        cargos = CargosClientes('email', tomar_remisiones=True, clientes_ids=[u'3636'], monto_minimo_mn=999999999)
        self.assertTrue(len(cargos) == 0, msg='se estan regresando cargos cuando el monto minimo es 0')

    def test_cargos_con_monto_minimo_sin_remissiones(self):
        """
        no deberia de dar cargos cuando el limite es 999999999 sin remisiones
        """
        cargos = CargosClientes('email', tomar_remisiones=False, clientes_ids=[u'4333'])
        self.assertTrue(len(cargos) == 0, msg='Cliente que solo deberia de tener remisiones esta regresando cargos con tomar remisiones como falso')

    def test_obtener_cargos_de_un_cliente_ids_dos_clientes(self):
        """
        Checa si la funcion regresa cargos de dos clientes espesificos con enteros
        """

        cargos = CargosClientes('email', clientes_ids=[3636, 3561], tomar_remisiones=True,)
        self.assertTrue(len(cargos) == 2)
