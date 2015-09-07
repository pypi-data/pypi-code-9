# -*- coding: utf-8 -*-


""" Modulo para extraçao de infomaçoes das paginas """


import logging

from bs4 import BeautifulSoup


logging.basicConfig(filename='epoca_crawler/Logs/problema_extracao.log', level=logging.ERROR)


#se link comeca com http verificar se e um link do website
def limita_dominio(link):
    dominio = "www.epocacosmeticos"
    if link[:4] == "http" and dominio in link:
        return True
    else:
        return False


def extrai_a(pagina):
    sopa = BeautifulSoup(pagina, 'lxml')  # ????? lxml
    resultado_a = sopa.findAll('a')
    return resultado_a


# se link acaba com '/p' e produto
# se produto envia para lista Produtos se nao para Gerais
def confere(link):
    if link[-2:] == "/p":
        return True
    else:
        return False


#recebe como parametro todos os attr's 'a'
def buscar_links(atributos_a):
    lista_busca = []
    for i in atributos_a:
        if i.has_attr('href'):
            lista_busca.append(i['href'])
    return lista_busca


#extrai informaçoes de paginas de produtos
def dados_produtos(pagina, link_pagina):
    lista_dados = [link_pagina]
    conteudo = BeautifulSoup(pagina, 'lxml')
    try:
        titulo = conteudo.title.text
        lista_dados.append(titulo)
        nome = conteudo.find('div', attrs={'class': 'name_brand'}).h1.text
        lista_dados.append(nome)
        return lista_dados
    except:
        logging.error("Erro na extração de dados da pagina: {0}".format(link_pagina))
        

