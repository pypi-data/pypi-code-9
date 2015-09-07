# -*- coding: utf-8 -*-


__version__ = "0.1"


"Crawler que extrai informaçoes de produtos do web site epocacosmeticos.com.br"


import csv
import os

from ferramentas_redes import requisicao
from retrying import retry
from extrator import *


todos = None  # variavel que ira receber a lista com todos os links
dados_finais = []  # recebe dados de produtos
link_principal = "http://www.epocacosmeticos.com.br/"
lista_links_produtos = []
lista_links_gerais = [link_principal]


minha_pasta = "epoca_crawler/Dados"


def retry_se_ioerror(e):
    return isinstance(e, IOError)


@retry(retry_on_exception=retry_se_ioerror)
def escreve(lista):
    with open(os.path.join(minha_pasta, "dados_ep.csv"), "wb") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["Link", "Titulo", "Nome"])
        print dados_finais
        for i in dados_finais:
            escritor.writerow([i[0].encode("utf-8"), i[1].encode("utf-8"), i[2].encode("utf-8")])

def main():
    for i in lista_links_gerais:

        try:
            pagina = requisicao(i)
            todos = buscar_links(extrai_a(pagina))
            
            for lnk in todos:
                if limita_dominio(lnk): # confere se o link pertence a epocacosmeticos.com.br

                    if lnk[0:4] != "http":
                        lnk_completo = "http://www.epocacosmeticos.com.br" + lnk
                    if confere(lnk) and lnk not in lista_links_produtos:
                        lista_links_produtos.append(lnk)
                        conteudo = requisicao(lnk)
                        dados_finais.append(dados_produtos(conteudo, lnk))
                        escreve(dados_finais)
                    else:
                        if lnk[-2:] != "/p" and lnk not in lista_links_gerais:
                            lista_links_gerais.append(lnk)
        except:
            pass

print main()
