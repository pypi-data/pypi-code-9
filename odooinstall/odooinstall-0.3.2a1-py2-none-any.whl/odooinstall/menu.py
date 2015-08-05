#-*- coding: utf-8 -*-

import os

# Definición del menú:

menu_actions={
    'main_menu': main_menu,
    '1': nueva_instancia,
    '2': listar_modulos,

}

def main_menu():
    """
    Menú de instalación de odoo y utilidades.
    """
    os.system('clear')

    print("Menú de instalación de odoo \n")
    print("Selecciona una acción: \n")
    print("--------------------------------\n")
    print("1.- Instalar nueva instancia.\n")
    print("2.- Listar módulos de una instancia.\n")
    print("--------------------------------\n")


def execute_menu(choice):
    os.system('clear')
    ch=choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print "Invalid selection, please try again.\n"
            menu_actions['main_menu']()


def nueva_instancia():
    os.system('clear')

def listar_modulos():
    os.system('clear')