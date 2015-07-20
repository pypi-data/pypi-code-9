#/home/mgfacioli/anaconda3/bin/python3.4
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        TesteFinDt
# Purpose:  Permite a realização de vários testes com o módulo FinDt, os quais
#       já podem servir como exemplo do seu uso.
#
# Author:      Marcelo
#
# Created:     16/08/2014
# Copyright:   (c) Marcelo 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

# Python module


# Own modules
from findt import FinDt

__author__ = """\n""".join(['Marcelo G Facioli (mgfacioli@yahoo.com.br)'])
__version__ = "3.0.1"


def main():
    """

    :rtype : object
    """
    var_path = "C:\\Apostilas\\Python\\BCB\\feriados_nacionais.csv"  # Home Version

    print("\n***Teste Modulo FinDt {}***\n".format(FinDt.__version__))
    dt_ini = '01/01/2015'
    dt_fim = '31/12/2015'

    seq = range(1, 100)
    teste = iter(seq)

    def format_test(fct):
        print("#" * 80, end="\n")
        print("### Teste {}".format(teste.__next__()))
        print(fct)
        print("#" * 80, end="\n\n")

    periodo = FinDt.DatasFinanceiras(dt_ini, dt_fim, path_arquivo=var_path)
    format_test(FinDt.DatasFinanceiras)
    format_test(type(periodo))
    format_test(periodo)

    format_test("Total de dias uteis no periodo selecionado: {}".format(len(periodo.dias())))
    format_test("Total de dias uteis no periodo selecionado: {}".format(len(periodo.dias(2))))
    format_test("Total de dias uteis no periodo selecionado: {}".format(len(periodo.dias(3))))

    format_test(periodo.dias(1, 'str'))
    format_test(periodo.lista_feriados('str'))
    format_test(periodo.lista_feriados())

    def teste_lista_feriados():
        fer = periodo.lista_feriados()
        for j in fer:
            print("Data: {}, {} .".format(j, fer[j]))

    format_test(teste_lista_feriados())

    # In[44]:
    def teste_lista_feriados2():
        fer = periodo.lista_feriados()
        for j in fer:
            print("Data: {}, {} .".format(FinDt.FormataData(j).data_para_str(), fer[j]))

    format_test(teste_lista_feriados2())

    # In[45]:
    format_test(periodo.dia_semana('23/01/2015'))

    # In[46]:
    format_test(periodo.primeiro_dia_mes('23/02/2015'))

    # In[47]:
    format_test(periodo.primeiro_dia_mes('23/02/2015', 'str'))

    # In[48]:
    format_test(periodo.ultimo_dia_mes('23/02/2015'))

    # In[49]:
    format_test(periodo.ultimo_dia_mes('23/02/2015', 'str'))

    # In[50]:
    format_test(periodo.lista_dia_especifico_semana(3))

    # In[51]:
    format_test(periodo.lista_dia_especifico_semana(3, 'str'))

    # In[68]:
    uteis_p_m = periodo.dias_uteis_por_mes()

    # In[65]:
    format_test(type(periodo.dias_uteis_por_mes()))

    # In[69]:
    #for per in uteis_p_m:
    #    print("Mês/Ano: {} - Dias Uteis: {}".format(per, uteis_p_m[per]))

    # In[55]:
    format_test(periodo.subperiodo("10/01/2015", "20/03/2015"))

    # In[54]:
    format_test(periodo.subperiodo("10/01/2015", "20/03/2015", dt_type='str'))

    # In[70]:
    #periodo.subperiodo("10/12/2014", "20/03/2015", dt_type='str')
    periodo.subperiodo("10/01/2015", "20/03/2016", dt_type='str')




"""
    # In[56]:
    subp = periodo.subperiodo("10/01/2015", "20/03/2015")
    len(subp)

    # In[57]:
    ######################
    ## Teste com set
    per1 = DatasFinanceiras("01/12/2013", "31/01/2014", path_arquivo=arqferiados)
    per2 = DatasFinanceiras("01/01/2014", "28/02/2014", path_arquivo=arqferiados)
    set1 = set(per1.dias())
    set2 = set(per2.dias())
    print(set1)

    # In[58]:
    setdiff = set1.difference(set2)
    print(setdiff)

    # In[59]:
    print(type(setdiff))

    # In[60]:
    set2diff = set2.difference(set1)
    print(set2diff)

    # In[61]:
    intersec = set1.intersection(set2)
    print(intersec)
"""

if __name__ == '__main__':
    main()






