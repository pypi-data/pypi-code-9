# -*- coding: utf-8 -*-
'''
Created on 28 Feb, 2015

@author: wangyi
'''
class Event(object):
    
    def __init__(self, portofolio, callback=None):
        self._portofolio = portofolio# for printer
        self.callback = callback

class FSM(object): 
    
    def __init__(self, *args, **kw):
        
        self.operant_dict = {}
        self.operant_list = []
        
        self.operant_stack = []
        self.tmpl_clist = []
        self.backup = []
        
        self._tmpl_events = []
        self._init_tmpl_events()

    def _init_tmpl_events(self):
        raise Exception("not implemented!")
    
#### helper for lookforward ####    
    # this is used when enconter special event, which need to lookforward 
    # this is to store pass data and position
    def lookforward(self, sign_in, sign_out, tokens):
        new_tokens = []
        index = 1# tokens[0] has been checked as sign_in
        while True:
            try:
                if tokens[index] is sign_out:
                    self.operate_stack.pop()
                    if self.operate_stack.__len__() != 0:
                        new_tokens.append(tokens[index])
                    else:
                        break
                elif tokens[index] is sign_in:
                    self.operate_stack.append(sign_in)
                    new_tokens.append(tokens[index])
                elif True:
                    new_tokens.append(tokens[index])
                index += 1
            except IndexError:
                break
        succ = index + 1
        return succ, new_tokens             
       
    def _runstack(self, root):
        stack = []
        stack.append((root, 0))
        while True:
            try:
                child, curr = stack.pop()
                self.process(child, curr, stack)
            except IndexError as e:
                break
            except TypeError as e:
                raise(e)# do some modifying here

#### helper for lookback #####            
            
            
#### states processing middleware #####
    def process(self, root, curr, stack):
        for event in self._tmpl_events:
            # next position
            succ = event.callback(curr, root[curr], root)
            if succ is None:
                continue
            stack.append((root, succ))
            

class Parser(FSM):
    
    DELIMITER = ','# THIS IS configurable
    
    def __init__(self, tmpl, *args, **kw):
        #super(FSM, self).__init__(*args, **kw)
        FSM.__init__(self, *args, **kw)
        self._tmpl = tmpl
        self.args, self.kw = args, kw
        
        self._init_opt()

    def _init_opt(self):
        try:
            self.DELIMITER = self.kw['DELIMITER']
        except:
            pass
    
    # override
    def _init_tmpl_events(self):
        self._tmpl_events = [
                             Event(portofolio='check empty', callback=self._check_empty),
                             Event(portofolio='multi/mass_data_population', 
                                   callback=self._proc_iter),
                             ]
 
#### callbacks ####
    def _check_empty(self, curr, key, tokens):
        if curr > len(tokens):
            raise IndexError('empty!')
           
    def _proc_iter(self, curr, key, tokens):
        # the simplest sate
        try:
            # %s+|?|*|[x]: minium states
            stack = [0]
            while True:
                child = stack.pop()
                char, next = key[child], key[child+1]
                if char == '%' and next == 's':
                    # replace mode, lookforward
                    if key[child+2] == '*':
                        pre, succ = key[0:child], key[child+3:]
                        v = self.DELIMITER.join(self.operant_list)
                        tokens[curr] = pre + v + succ
                        child += 3 + len(v)
                        stack.append(child)
                    # elif
                    else:
                        tokens[curr] = self.operant_list.pop(0)
                        child += 2
                        stack.append(child)
                else:
                    child += 1
                    stack.append(child)
        except IndexError:
            pass
        else:
            pass
        succ = curr + 1 
        return succ      

#### main loop
    # this is the data parser to prepare or parse data for populating after the passed string format is analyzed.
    def parse(self, data, tmpl=None):
        # for simplicity
        tokens = self._parse(data, tmpl)
        return self._str(tokens)        

#### load data ####                   
    def load(self, *args, **kw):
        pass
    
    def load_arr(self, arr):
        for item in arr:
            self.operant_list.append(str(item))
            
    def load_data(self, data_str):
        pass
#### parse tmpl ####
    # begin is the main loop
    # this method is called by data_parse    
    def _parse(self, data, tmpl=None):
        # for simplicity, currently use data
        self.load_arr(data)   
        tokens = self.tokenize(tmpl or self._tmpl)
        self._runstack(tokens)
        return tokens

    @staticmethod
    def tokenize(tmpl):
        def _filter(item):
            if item not in ('',' ', '\n', '\t'):
                return True
            return False
        
        tokens = []
        for word in tmpl.lstrip("\t ").split(' '):
            tokens.append(word)
        return list(filter(_filter, tokens))
    
    def _str(self, tokens=None):
        if tokens is None:
            return self
        return ' '.join(tokens)
    
if __name__ == "__main__":
    a = Parser("INSERT A \n%s*", DELIMITER='\n').parse([1,2,3,4,5,6])
    print(a)