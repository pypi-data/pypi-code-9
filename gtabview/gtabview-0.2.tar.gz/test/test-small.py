# --- view a list
from pylab_local import *
import gtabview
tv([1, 2, 3])

# --- view a list (transposed)
from pylab_local import *
import gtabview
tv([1, 2, 3], transpose=True)

# --- view a dict (by columns)
from pylab_local import *
import gtabview
d = {'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}
tv(d)

# --- dict (by rows)
from pylab_local import *
import gtabview
d = {'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}
tv(d, transpose=True)

# --- view a simple list of lists (no header)
from pylab_local import *
import gtabview
tv([['a', 'b', 'c'], [1, 2, 3], [4, 5, 6], [7, 8, 9]])

# --- view a simple list of lists (with header)
from pylab_local import *
import gtabview
tv([['a', 'b', 'c'], [1, 2, 3], [4, 5, 6], [7, 8, 9]], hdr_rows=1)

# --- view a simple list of lists (transposed)
from pylab_local import *
import gtabview
tv([['a', 'b', 'c'], [1, 2, 3], [4, 5, 6], [7, 8, 9]], hdr_rows=1, transpose=True)

# --- a simple DF
from pylab_local import *
import gtabview
tv(pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))

# --- DF with columns
from pylab_local import *
import gtabview
tv(pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], columns=['a', 'b', 'c']))

# --- DF with multiindex
from pylab_local import *
import gtabview
arrays = [['bar', 'bar', 'baz', 'baz', 'foo', 'foo', 'qux', 'qux'],
          ['one', 'two', 'one', 'two', 'one', 'two', 'one', 'two']]
tuples = list(zip(*arrays))
index = pd.MultiIndex.from_tuples(tuples, names=['first', 'second'])
arrays2 = [['bar', 'bar', 'bar', 'bar', 'baz', 'baz', 'baz', 'baz'],
           ['foo', 'foo', 'qux', 'qux', 'foo', 'foo', 'qux', 'qux'],
           ['one', 'two', 'one', 'two', 'one', 'two', 'one', 'two']]
tuples2 = list(zip(*arrays2))
index2 = pd.MultiIndex.from_tuples(tuples2, names=['first', 'second', 'third'])
df = pd.DataFrame(np.random.randn(8, 8), index=index2, columns=index)
tv(df)

# --- PD Series
from pylab_local import *
import gtabview
tv(pd.Series([1,2,3]))

# --- NP array (1 dimension)
from pylab_local import *
import gtabview
tv(np.array([1,2,3]))

# --- NP array
from pylab_local import *
import gtabview
tv(np.array([[1,2,3], [4,5,6]]))

# --- NP matrix
from pylab_local import *
import gtabview
tv(np.matrix([[1,2,3], [4,5,6]]))

# --- NP 3d matrix
from pylab_local import *
import gtabview
arr = np.array(np.random.random((3,3,2)))
tv(arr)
