# -*- coding: utf-8 -*-


def printLista(lista, nivel = 0):
    for elemento in lista:
        if isinstance(elemento, list):
            printLista(elemento, nivel + 1)
        else:
            for numero in range(nivel):
                print("\t", end = '')
            print(elemento)


