# The MIT License (MIT)
#
# Copyright (c) 2015 by Teradata
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import teradata
import gc

udaExec = teradata.UdaExec(appName="MemoryLeak", version="1.0")

def td_connect():
    return udaExec.connect(method="odbc", system="paper", username="dbc", password="dbc")

def some_function ():
    conn = td_connect();
    curs = conn.cursor();
    curs.execute("SELECT * FROM DBC.Roles")
    curs.close()
    conn.close()

for i in range(3):
        print
        print('iteration number: {}'.format(i))
        n = gc.collect()
        print("   uncollectable garbage objects: {}, shown here:".format(len(gc.garbage)))
        print("       " + str(gc.garbage))
        referrers = gc.get_referrers(*gc.garbage)
        print("   referrers to uncollectable garbage: {}, shown here:".format(len(referrers)))
        for single_referrer in referrers:
            print("       " + str(single_referrer))
        some_function()
