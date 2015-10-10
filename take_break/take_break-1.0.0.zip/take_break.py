import webbrowser
import time

total_breaks=3
break_count=0
print("Program Start Time:"+time.ctime())
while(break_count<total_breaks):
    time.sleep(5)
    webbrowser.open("https://www.youtube.com/watch?v=HXsC9r-hYzg",1,autoraise="true")
    break_count=break_count+1
