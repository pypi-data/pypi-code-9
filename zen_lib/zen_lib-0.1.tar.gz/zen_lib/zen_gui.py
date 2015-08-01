# -*- coding:utf-8 -*-
import Tkinter 
import tkMessageBox
import tkFileDialog
import tkColorChooser
import tkSimpleDialog
"""
20150412 重构
"""
def set_hotkey_handler(hotkey_proc="""
    Demo 
    def hotkey_proc(event):
        tmp = event.char
        if tmp == "n":
            show_next()
        elif tmp == "h":
            copyto_best()
    """):

    global root
    root.bind("<Key>", hotkey_proc)
def init_gui(title_name=u"未定义程序标题", is_top=False):
    global root, dict_hotkey
    root = Tkinter.Tk(className=title_name)
    dict_hotkey = {}
    
    if is_top:
        root.wm_attributes("-topmost", 1)
    return root
def add_hotkey(key="n", event=None):
    if event == None:
        dict_hotkey[key] = msgbox
    else:
        dict_hotkey[key] = event
        
def msgbox(show_title=u"未定义按钮事件", show_str=u"未定义文本"):
    return tkMessageBox.showinfo(show_title, show_str)
def inputbox(title=u"未定义标题", prompt=u"未定义提示"):
    return tkSimpleDialog.askstring(title=title, prompt=prompt)
def add_button(bt_name=u"未命名", new_function=msgbox, width=20, height=2):
    tmp_button = Tkinter.Button(root, 			
			anchor="center",  # 指定文本对齐方式
			text=bt_name,  # 指定按钮上的文本
			width=width,  # 指定按钮的宽度，相当于40个字符
			height=height,
                        command=new_function)  # 指定按钮的高度，相当于5行字符
    tmp_button.pack()
    return 

def add_button_var(bt_name=u"未命名", new_function=msgbox, width=20, height=2):
    varstr = Tkinter.StringVar()
    varstr.set(bt_name)
    bt = Tkinter.Button(root,
                            anchor="center",  # 指定文本对齐方式
                            textvariable=varstr,  # 指定按钮上的文本
                            width=width,  # 指定按钮的宽度，相当于40个字符
                            height=height,  # 指定按钮的高度，相当于3行字符
                            command=new_function)  # 处理函数
    bt.pack()
    return varstr


def add_label(show_str=u"未定义label"):
    var = Tkinter.StringVar()
    var.set(show_str)
    label = Tkinter.Label(root, textvariable=var, wraplength=240, justify='left')
    label.pack()
    return var
def add_edittext(show_str=u"未定义entry", width=20):
    var = Tkinter.StringVar()
    var.set(show_str)
    en = Tkinter.Entry(root, textvariable=var, width=width)
    en.pack()
    return var
def add_canvas(width=640, height=480):
    canvas = Tkinter.Canvas(root,
                            width=width,  # 指定Canvas组件的宽度
                            height=height,  # 指定Canvas组件的高度
                            bg='white')  # 指定Canvas组件的背景色
    canvas.pack(side=Tkinter.LEFT)
    return canvas

def chooser_directory(title=u"选择处理目录,不选择视同选择当前目录,自动添加os.sep"):
    import os
    tmp_path = tkFileDialog.askdirectory(title=title)
    if tmp_path == "":
        return os.curdir + os.sep
    else:
        return tmp_path.replace("/", os.sep) + os.sep
    
def chooser_file_open(title=u"未定义标题", file_type='*.txt *.zen'):  # 按钮事件处理函数
    r = tkFileDialog.askopenfilename(title=title,  # 创建打开文件对话框
			filetypes=[('zen_data', file_type), ('All files', '*')])  # 指定文件类型为Python脚本
    return r  # 输出返回值
def chooser_file_save(title='Output Choose', initialdir=r'D:\\', initialfile='ouput_data.txt'):  # 按钮事件处理函数
    r = tkFileDialog.asksaveasfilename(title=title, initialdir=initialdir, initialfile=initialfile)
    return r
def chooser_color(title=u"Zen Color Choose"):  # 按钮事件处理函数
    r = tkColorChooser.askcolor(title=title)  # 创建颜色选择对话框
    return r  # 输出返回值
def mainloop():
    root.mainloop()
if __name__ == "__main__":
    init_gui(u"ZenGUIDemo", True)
    add_button(u"动态添加新按钮", add_button)
    add_button(u"颜色选择器", chooser_color)
    add_button(u"测试选择目录", chooser_file_open)
    add_button(u"测试选择写入文件", chooser_file_save)
    add_button(u"测试选择写入目录", chooser_directory)
    ee = add_edittext()
    ee.set(u"测试写入entry")
    aa = add_label()
    aa.set(u"测试label")
    root.mainloop()
