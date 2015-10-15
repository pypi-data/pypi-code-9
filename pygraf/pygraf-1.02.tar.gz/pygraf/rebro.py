__author__ = 'dwliv_000'
class rebro:# ����� ����� �����(��� �������� ����� ����� ��� ���������� �����)
    def __init__(self,u,v,c):
        self.__first=u
        self.__second=v
        self.__ves=c
    def change_ves(self,c):
        self.__ves=c

    def get_first(self):
        return self.__first

    def get_second(self):
        return  self.__second

    def get_cost(self):
        return self.__ves