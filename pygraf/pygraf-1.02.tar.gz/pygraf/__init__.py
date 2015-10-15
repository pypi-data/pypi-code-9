__author__ = 'dwliv_000'
from pygraf.rebro import *
#coding:utf-8
class graf:

    def __init__(self,n,mas): # inzilize graf(n-count point,mas =[[1,2]...] massive [point,point]
        self.__graff={}#массив графа в виде словаря
        self.__count=n
        link=self.__graff
        self.__mas_comp=[]
        self.__inf=200000000
        self.__mas_rebr=[]#массив ребер
        for j in mas:
            if j[0] not in link.keys():
                link[j[0]]=[j[1]]
            else:
                link[j[0]].append(j[1])
            if len(j)==3:
                reb=rebro(j[0],j[1],j[2])
            else:
                reb=rebro(j[0],j[1],0)
            self.__mas_rebr.append(reb)

    def check_orient(self):#проверяем ориентированность графа  #false - ориентирован #true-неоринтирован
        link=self.__graff
        for j in link.keys():
            for k in link[j]:
                if k not in link.keys():
                    return False
                else:
                    if j not in link[k]:
                        return False
        return True

    def dfs(self,u,step):#прогоняем поиск в глубины для u-ой вершины
        if step==0:
            self.__dfsmas=[]
            dfslink=self.__dfsmas
            for j in range(self.__count):
                dfslink.append(False)
        self.__dfsmas[u-1]=True
        if u in self.__graff.keys():
            for j in self.__graff[u]:
                if self.__dfsmas[j-1]==False:
                    self.dfs(j,step+1)

    def print_dfs(self):#пишем dfs путь
        try:
            return self.__dfsmas
        except:
            return 'Не инциализирован DFS - funtcion print_dfs'


    def change_cost(self,u,v,c):
        for j in self.__mas_rebr:
            if j.get_first()==u and j.get_second()==v:
                j.change_ves(c)
                break

    def comp(self,needpr):#компонента связанности для неоринтированного графа
        if not self.check_orient():
            return False
        else:
            k=0
            for j in range(self.__count):
                self.__mas_comp.append(False)
            for j in range(self.__count):
                if self.__mas_comp[j]==False:
                    k=k+1
                    self.dfs(j+1,0)
                    for m in range(len(self.__dfsmas)):
                        if self.__dfsmas[m]==True:
                            self.__mas_comp[m]=True
                            if needpr==True and m!=j:
                                print(j+1,'-->',m+1)
            return k

    def minwayves_wihtout_cicly(self,u,v):
        d=[]
        m=len(self.__mas_rebr)
        e=self.__mas_rebr
        for j in range(self.__count+1):
            d.append(self.__inf)
        d[u]=0
        for i in range(1,self.__count+1):
            any = False
            for j in range(m):
                if (d[e[j].get_first()] < self.__inf):
                    if (d[e[j].get_second()] > d[e[j].get_first()] + e[j].get_cost()):
                        d[e[j].get_second()] = d[e[j].get_first()] + e[j].get_cost()
                        any = True
            if any==False:
                break
        if v!=u:
            print(d[v]) if d[v] != self.__inf else print('Havent path')
        else:
            print(d)

    def minwayprint_wihtout_cicly(self,u,v):
        d=[]
        p=[]
        m=len(self.__mas_rebr)
        e=self.__mas_rebr
        for j in range(self.__count+1):
            d.append(self.__inf)
            p.append(-1)
        d[u]=0
        for i in range(1,self.__count+1):
            any = False
            for j in range(m):
                if (d[e[j].get_first()] < self.__inf):
                    if (d[e[j].get_second()] > d[e[j].get_first()] + e[j].get_cost()):
                        d[e[j].get_second()] = d[e[j].get_first()] + e[j].get_cost()
                        p[e[j].get_second()] = e[j].get_first()
                        any = True
            if any==False:
                break


        if (d[v] == self.__inf):
            print('Havent path from',u,'to',v);
        else:
            path=[]
            cur=v
            while cur!=-1:
                path.append(cur)
                cur=p[cur]
            path.reverse()
            print('Path from',u,'to',v);
            for j in range(len(path)):
                print(path[j],end=' ')
            print()
    def print_graff(self):
        print(self.__graff)
    def del_rebro(self,u,v):
        if u not in self.__graff.keys():
            print('Didnt use')
        else:
            if v not in self.__graff[u]:
                print('Didnt use')
            else:
                self.__graff[u].remove(v)
                for j in self.__mas_rebr:
                    if j.get_first()==u and j.get_second()==v:
                        self.__mas_rebr.remove(j)
                        del j
                        break
                #print('Ребро удаленно')
    def add_rebro(self,u,v,c):
        if u not in self.__graff.keys():
            self.__graff[u]=[v]
            reb=rebro(u,v,c)
            self.__mas_rebr.append(reb)
            #print('Ребро добавлено')
        else:
            if v not in self.__graff[u]:
                self.__graff[u].append(v)
                reb=rebro(u,v,c)
                self.__mas_rebr.append(reb)
                #print('Ребро добавлено')
                #print('Ребро уже есть в списке')




