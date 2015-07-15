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


from . import *


banco_itau = Banco('341', 'Banco Itaú')

class ItauBoleto(Boleto):

    def _validar_codigo_barras(self):
        """
        Como a classe ancestral já valida os campos padronizados pela FEBRABAN basta
        validar os campos necessários ao Campo Livre.
        """
        super(ItauBoleto, self)._validar_codigo_barras()
        Boleto._validar_digitos(self.convenio.carteira, 3, 'carteira')
        Boleto._validar_digitos(self.convenio.agencia, 4, 'agência', True)
        Boleto._validar_digitos(self.convenio.conta, 5, 'conta', True)

    @property
    def campo_livre(self):
        """
        Gera o campo livre do código de barras.
        """
        agencia_conta = "%4s%5s" % (self.convenio.agencia[:-2], self.convenio.conta[:-2])
        campo_livre = "%3s%s%1s%4s%5s%1s000" % (self.convenio.carteira,
                                                self.nosso_numero,
                                                modulo10("%s%3s%8s" %
                                                         (agencia_conta, self.convenio.carteira, self.nosso_numero)),
                                                self.convenio.agencia[:-2],
                                                self.convenio.conta[:-2],
                                                modulo10(agencia_conta))
        return campo_livre
