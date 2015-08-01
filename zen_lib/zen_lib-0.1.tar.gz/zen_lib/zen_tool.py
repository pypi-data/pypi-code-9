# coding:utf-8
import threading, os, time, thread

# 
global z
"""
import sys
sys.path.append("D:\\icbc\\icbc_coding\\")
import zen_tool
z=zen_tool.z

20141209 最新版本，之后无更新 仅仅因导入问题
20150411 重构开始，暂停serial和pygame的引用
20150724 修改filter_flist中多参数的bug
"""
class zen_tool(): 
    instance = None 
    mutex = threading.Lock()
    debug_flag = 0
    def __init__(self):
        global debug_flag
        debug_flag = 0
    @staticmethod
    def getInstance(): 
        if(zen_tool.instance == None): 
            zen_tool.mutex.acquire()  
            if(zen_tool.instance == None): 
                zen_tool.instance = zen_tool() 
            else:
                pass
            zen_tool.mutex.release() 
        else: 
            # printInfo('单例已经初始化')
            pass
        return zen_tool.instance
    def dbp(self, message):
        if self.debug_flag > 0:
            print message
    def dbi(self, message):
        if self.debug_flag > 1:
            print message
    def dbe(self, message):
        if self.debug_flag > 2:
            print message
    def load_data(self, filename, sep=None):
        f = open(filename, "r")
        tmp = []
        if sep == None:
            for i in f:
                tmp.append(i)
        else:
            for i in f:
                tmp.append(i.split("\t"))
        f.close()
        return tmp
    def format_time(self, time_current=None, time_format="%Y%m%d_%H:%m:%S"):
        if time_current == None:
            time_current = time.time()
        
        return time.strftime (time_format, time.localtime(time_current))
    def format_time_mili(self, time_current=None, time_format="%Y%m%d_%H%m%S_"):
        if time_current == None:
            time_current = time.time()
        return time.strftime (time_format, time.localtime(time_current)) + str(round(time.time() % 1, 3))
    def sleep(self, t=0.1):
        time.sleep(t)
        

    def random(self, end=100, start=0):
        import random
        return random.randint(start, end)
        pass
#     def serport(self, com="com3"):
#         try:
#             ser = serial.Serial(com, 115200, timeout=1)
#         except :
#             ser = False
#         return ser
    def new_thread(self, function_name, function_params=()):
        """
        example:needexit_thread() 
        thread.start_new_thread(timer, (2,2))
        thread.exit_thread()
        """
        thread.start_new_thread(function_name, function_params)
    def get_file_list(self, folder=os.getcwd(), filetype=None):
        # print folder
        # print os.listdir(folder)
        result = os.listdir(folder)
        if not filetype == None:
            result = self.fliter_filetype(filetype, result)
        return result
    def fliter_filetype(self, ft, data):
        """
        exmaple:
        flist=fliter_filetype(["txt"],filelist)
        """
        
        filetypes = []
        if type(ft) == str:
            filetypes.append("." + ft)
        elif type(ft) == list:
            for i in ft:
                if type(i) == str:
                    filetypes.append("." + i)
        self.dbp(filetypes)
        data_output = []
        for i in data:
            for tp in filetypes:
                if i.count(tp) > 0:
                    data_output.append(i)
                    continue
                    
        self.dbp(data_output)
        return data_output
    def get_md5(self, string):
        from hashlib import md5
        m = md5()
        m.update(string)
        return m.hexdigest() 
       
     
    def get_file_md5(self, filename):
        from hashlib import md5
        m = md5()
        f = open(filename, 'rb')
        m.update(f.read())
        f.close()
        return m.hexdigest()

    def grab(self, filename=None):
        from PIL import ImageGrab
        img = ImageGrab.grab()
        if filename == None:
            filename = self.format_time_mili()
        img.save(filename + ".png", "PNG")
        
    def exist(self, filename):
        return os.path.exists(filename)
    def isdir(self, filename):
        return os.path.isdir(filename)
    def folder(self, path):
        if os.path.exists (path):
            return path
        else:
            os.mkdir(path)
            return path
            
        pass
#     def mp3_play(self, filename="r:\\1.mp3"):
#         import pygame
#         pygame.mixer.init()
#         pygame.mixer.music.load(filename)
#         pygame.mixer.music.play()
        # while pygame.mixer.music.get_busy():
        #    m = pygame.mixer.music.get_pos()
        #    print m
        #    time.sleep(0.1)
    def tts_speak(self, word=u"语音功能成功加载"):
        # 需windows下使用
        try:
            from win32com.client import DispatchEx
            self.tts.tts_speak(word)
        except:
            self.tts = DispatchEx("SAPI.SpVoice")
            print "tts service init，this function should be used in windows"
            self.tts.speak(word)
    def save_object(self, filename, obj):
        import pickle
        a = open(filename, "w")
        a.write(pickle.dumps(obj))
        a.close()
        return "Done"
    
    def load_object(self, filename):
        import pickle
        result = None
        if self.exist(filename):
            f = open(filename)
            result = pickle.loads(f.read())
            f.close()
        return result
    def kv_get(self):
        pass
    def kv_put(self):
        pass
    def kv_save(self):
        pass
    
    
    
z = zen_tool.getInstance()
if __name__ == "__main__":
    print "zen_tool_init:", z.format_time()
    z.tts_speak(u"Zen_tool 作为主程序启动")
    
