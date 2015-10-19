

import threading
import magic
m = magic.Magic()

def doit():
    for i in range(100):
        magic.from_file("test/testdata/test.pdf")

t = []
for i in range(100):
    tr = threading.Thread(target=doit)
    t.append(tr)
    tr.start()

for j in t:
    j.join()

    
