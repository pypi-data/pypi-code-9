'''
sxclient SX client-side library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

sxclient is a library which implements methods for communicating with an SX
cluster. Using provided objects and functions, it is possible to prepare and
send a series of queries as per the API documentation at
<http://docs.skylable.com/>.

Example usage:

   >>> import sxclient
   >>> cluster = sxclient.Cluster('my.cluster.example.com')
   >>> user_data = sxclient.UserData.from_key_path('/path/to/my/keyfile')
   >>> with sxclient.ClusterSession(cluster, user_data) as session:
   ...     content = sxclient.listUsers(cluster, session)

Copyright (c) 2015 Skylable Ltd.
License: Apache 2.0, see LICENSE for more details.

'''

import operations
from .operations import *
from .models import Cluster, UserData
from .queries import ClusterSession

__all__ = ['Cluster', 'ClusterSession', 'UserData']
# Expose all the specific operation functions.
__all__.extend(operations.__all__)
