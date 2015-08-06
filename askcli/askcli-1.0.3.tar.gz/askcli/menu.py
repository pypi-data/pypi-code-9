# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from askcli.item import Item

class Menu(object):
    '''
    permet de faire un menu à choix
    '''
    title = ''
    _choice = list()
    choose = None
    _choose_index = -1
    case = False

    def __init__(self, choice, title='', case=False):
        '''
        :param Item[] choice: liste de ``menu.Item`` des choix possible. acceptable une liste de str
        :param str tilte: titre du menu
        :param bool case: menu sensible à la casse (miniscule/majuscule)

        :raise ValueError: si choice n'est pas une liste. Si un element dans la liste n'est pas de type Item ou Str

        permet d'initialiser les attribut de l'objet.

         * **choose** Liste des choix possible
         * **choice** Choix effectuer. par défaut -1. est automatiquement seter quand on appel la méthode launch()
         * **title**  Titre du menu *optionnel*
         
        '''
        self._choice = list()

        if isinstance(choice, list):
            loop = 1

            for i in choice:

                if type(i).__name__ == 'Item':
                    self._choice.append(i)
                elif isinstance(i, ''.__class__):
                    i = str(i)
                    self._choice.append(Item(loop, i))
                else:
                    raise ValueError('the index {0} in list is [{1}]. This type are not suported'.format(loop-1, type(i).__name__))

                loop += 1
        else:
            raise ValueError('The first argument [choice] must be list type. {0} are not suported'.format(type(choice).__name__))

        self.title = str(title)
        self.case = bool(case)
        self.choose = -1

    def __repr__(self):
        return "<askcli.menu {0} choice>".format(len(self._choice))

    def __str__(self):
        if len(self.title) == 0:
            value = ''
        else:
            value = '> ' + self.title

        for item in self._choice:
            value += "\n  {0}".format(item)

        return value

    def launch(self, text='input', err='error key, (unavailable)'):
        """
        :param str text: text à afficher avant la saisie. par Défaut **choix**. Ne pas insérer le ' : ' à la fin.
        :param str err: text à afficher en cas d'erreur de saisie. Par Défaut **X - Saisie incorrecte, merci de selectionner une valeur dans le champ**.

        permet de lancer le menu avec la saisie à la fin.
        Des tests sont fait sur la saisie, si la valeur est 
        """

        print(self.__str__())

        ask = True
        while ask:
            key = input('? {0} : '.format(text))

            if self.key_is_ok(key):
                ask = False
                self._set_choice(key)
            else:
                ask = True

            if ask:
                print(' X - {0}'.format(err))

    def get_choosen_text(self):
        """
        :rtype: str
        :return: le texte choisi
        
        si ``self.choose`` est inferieur à **0** alors on retourn une chaine vide ''
        """

        if self._choose_index > -1:
            return self._choice[self._choose_index].txt
        else:
            return ''

    def key_is_ok(self, key):
        '''
        :param str key: clef à tester

        :return: si la clef est présente dans la liste de choix
        :rtype: bool

        permet de tester si le cled ``key`` est présent dans la liste de choix.
        prise en compte de la case si ``self.case = True``
        '''
        try:
            key = str(key)
        except Exception:
            return False

        index = 0
        loop = True
        is_ok = False
        while loop:

            if index > (len(self._choice)-1):
                loop = False

            elif (self.case and self._choice[index].key == key) or \
               (not self.case and self._choice[index].key.lower() == key.lower()):
                is_ok = True
                loop = False
                self._choose_index = index

            else:
                is_ok = False
                index += 1

        return is_ok


    def _set_choice(self, choose):
        """
        :param str choose: choix que l'on souhaite affecter à cette liste.

        :raise ValueError: si la clef ``choose`` n'est pas présent dans la list
        """

        choose = str(choose)
        if self.key_is_ok(choose):
            self.choose = choose
        else:
            self._choose_index = -1
            raise ValueError("the key {0} are not in choice list".format(choose))

