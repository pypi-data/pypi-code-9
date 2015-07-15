# -*- coding: utf-8 -*-
"""
The MIT License (MIT)

Copyright 2015 Umbrella Tech.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
__author__ = 'Kelson da Costa Medeiros <kelsoncm@gmail.com>'


from pyaboleto import *


banco_caixa = Banco('104', 'Caixa')

class CaixaBoleto(Boleto):

    def _validar_codigo_barras(self):
        """
        Como a classe ancestral já valida os campos padronizados pela FEBRABAN basta
        validar os campos necessários ao Campo Livre.
        """
        super(CaixaBoleto, self)._validar_codigo_barras()

        self._validar_digitos(self.convenio.numero, 6, 'código do beneficiário', True)
        self._validar_digitos(self.nosso_numero, 17, 'nosso número')
        raiser(self.nosso_numero[0] not in ('1', '2'), 'O primeiro digito do nosso número deve ser 1 ou 2.')
        raiser(self.nosso_numero[1] != '4', 'O segundo digito do nosso número deve ser 4.')

    @property
    def campo_livre(self):
        """
        Gera o campo livre do código de barras.
        """
        self._validar_codigo_barras()
        sem_dv = -2
        campo_livre = '%6s%1s%3s%1s%3s%1s%9s' % (self.convenio.numero[:sem_dv],
                                                 self.convenio.numero[-1],
                                                 self.nosso_numero[2:5],
                                                 self.nosso_numero[0],
                                                 self.nosso_numero[5:8],
                                                 self.nosso_numero[1],
                                                 self.nosso_numero[8:17])
        dv_campo_livre = modulo11(campo_livre)
        return campo_livre + dv_campo_livre
