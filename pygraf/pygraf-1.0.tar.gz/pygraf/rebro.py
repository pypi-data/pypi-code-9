__author__ = 'dwliv_000'
class rebro:# класс ребро графа(для хранения ребер графа для кратчайших путей)
    def __init__(self,u,v,c):
        self.first=u
        self.second=v
        self.ves=c
