# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from askcli import Item 

class AskBool(object):

    desc = ''
    valid = None
    invalid = None
    required = True
    default = False
    choosen = None


    def __init__(self, desc, v_text='Yes', i_text='No', v_key=None, i_key=None, required=True, default=False):
        """
        :param str desc: ce que écris le champs
        :param str v_text: text qui corespond à vrai 
        :param str i_text: text qui corespond à faux 
        :param str v_key: caractères de saisie qui sera valide (en plus du v_text) par défaut permier lettre de v_text
        :param str i_key: caractères de saisie qui sera valide (en plus du i_text) par défaut  permier lettre de i_text
        :param bool required: si faux alors il doit y avoir une valeur par défaut
        :param bool default: valeur par défaut
        """
        self.desc = str(desc)
        self.required = bool(required)
        self.default = bool(default)

        if isinstance(v_text, Item):
            self.valid = v_text
        else:
            v_text = str(v_text)

            if v_key is None and v_text:
                v_key = str(v_text[0])

            self.valid = Item(v_key, v_text)

        if isinstance(i_text, Item):
            
            self.invalid = i_text

        else:
            if i_key is None and i_text:
                i_key = str(i_text[0])
            
            self.invalid = Item(i_key, i_text)
        
        self.choosen = None


    def __repr__(self):
        """
        :rtype: str
        :return: representation de l'objet
        """
        return "<askcli.AskBool : {0}  [{1}/{2}]>".format(self.desc, self.valid.key, self.invalid.key)

    def __str__(self):
        """
        :rtype: str
        :return: représentaion to string de l'objet
        """

        return "{0}  [{1}/{2}] : ".format(self.desc, self.valid.key, self.invalid.key)

    def _get_valid_array(self):
        """
        :return: une list avec touts les champs da validation possible
        :rtype: list 
        """
        return [self.valid.txt.lower(), self.valid.key.lower()]


    def _get_invalid_array(self):
        """
        :return: une list avec touts les champs da validation possible
        :rtype: list 
        """
        return [self.invalid.txt.lower(), self.invalid.key.lower()]


    def key_is_valid(self, key):
        """
        :param str key: clef à tester

        :rtype:bool
        :return: si la clef est valable ou non
        """

        try:
            key = str(key).lower()
        except Exception as e:
            return False
        
        valid = self._get_valid_array() + self._get_invalid_array()

        return (key in valid)

    def set_choice(self, key):
        """
        :param str key: clef que l'on souhaite affecter

        :Exception valueError: si la key n'est pas valide
        """

        key = str(key).lower()
        if self.key_is_valid(key):
            if key in self._get_valid_array():
                self.choosen =  True
            else:
                self.choosen =  False

        else:
            raise ValueError("askcli.AskBool : error key [{0}]. Is not valide ".format(key))

    def get_resp(self):
        """
        :return: si l'utilisateur à choisi le choix vraix ou False
        :rtype: bool

        :Exception: si choosen est a None
        """
        
        if self.choosen is None:
            raise Exception

        if isinstance(self.choosen, bool):
            return self.choosen
        else:
            raise Exception("askcli.AskBool : Unexpected value for self.choosen")

    def get_text(self):
        """
        :return: Le texte en fonction du choi
        :rtype: str
        """
        
        try:
            if self.get_resp():
                return self.valid.txt
            else:
                return self.invalid.txt
        except Exception as e:
            return ''

    def launch(self, show_text_key=False, err_mess="error key"):
        '''
        :rtype: bool
        :return: vrai si il è choisi le t_key

        Permet de lancer la demande de saisie à l'utilisateur
        '''

        if show_text_key:
            print("   [{0}] {1} ".format(self.valid.key, self.valid.txt))
            print("   [{0}] {1} ".format(self.invalid.key, self.invalid.txt))
        
        if not self.required and show_text_key:
            def_explain = "   Default : [{0}]"
            if self.default:
                print(def_explain.format(self.valid.key))
            else:
                print(def_explain.format(self.invalid.key))

        askprint = " ? {0} [{1}/{2}] : "

        if not self.required:
            if self.default:
                t_key = self.valid.key.upper()
                f_key = self.invalid.key.lower()

            else:
                f_key = self.invalid.key.upper()
                t_key = self.valid.key.lower()
        else:
            f_key = self.invalid.key.lower()
            t_key = self.valid.key.lower()


        ask = True
        while ask:
            key = raw_input(askprint.format(self.desc, t_key, f_key))

            if self.required:
                if self.key_is_valid(key):
                    self.set_choice(key)
                    ask = False
                else:
                    ask = True

            else:
                if not key:
                    ask = False
                    mess_back = " > set default Value : {0}"
                    if self.default:
                        def_value = self.valid.key
                    else:
                        def_value = self.invalid.key

                    self.set_choice(def_value)
                    print(mess_back.format(def_value))
                else:
                    if self.key_is_valid(key):
                        self.set_choice(key)
                        ask = False
                    else:
                        ask = True

            if ask:
                print(' x {0}'.format(err_mess))

        return self.get_resp()
