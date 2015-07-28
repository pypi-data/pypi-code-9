# kvpbase Python SDK Test Application
#
#
# Requires installation of requests:
# 
# $ pip install requests
# C:\Python34\Scripts> easy_install requests
#
# For more information, see: http://docs.python-requests.org/en/latest/user/install/
#
#
# Uncomment the tests you wish to perform below
# Replace your user GUID, API key, and endpoint in the constructor to point to your
# user account on an appropriate kvpbase node

import os
import sys

from kvpbase import kvpbase
from kvpbase import response

print("===============================================================================")
print("")
print("kvpbase Python SDK Test Application")
print("")
print("===============================================================================")

kvp = kvpbase("user_guid", "api_key", "https://api1.kvpbase.com:443/")
incl_resp_body = True
# incl_resp_body = False

# Retrieve an object, change path to match a valid or invalid object
# resp = kvp.get_obj("hello_python.txt")
# resp = kvp.get_obj("path/to/container/hello_python.txt")

# Create container
# resp = kvp.create_container("test_container")
# resp = kvp.create_container("path/to/container")

# Retrieve container
# resp = kvp.get_container("");
# resp = kvp.get_container("path/to/container")

# Create an object with specific name
# resp = kvp.create_obj_specific_name("hello_python.txt", "Hello Python!", "text/plain")
# resp = kvp.create_obj_specific_name("path/to/container/hello_python.txt", "Hello Python!", "text/plain")

# Create an object with system-assigned name
# resp = kvp.create_obj_system_name("", "Hello Python!", "text/plain")
# resp = kvp.create_obj_system_name("path/to/container", "Hello Python!", "text/plain")

# Delete an object
# resp = kvp.delete_obj("hello_python.txt")
# resp = kvp.delete_obj("path/to/container/hello_python.txt")

# Delete container
# resp = kvp.delete_container("path/to/container")

# Verify container exists
# resp = kvp.container_exists("test_container")
# resp = kvp.container_exists("path/to/container")

# Verify object exists
# resp = kvp.obj_exists("hello_python.txt")
# resp = kvp.obj_exists("path/to/container/hello_python.txt")

# Move object
# resp = kvp.move_obj(["path","to","container"], "original_name.txt", ["path","to","container"], "new_name.txt")

# Move container
# resp = kvp.move_container(["path","to",], "original_name", ["path","to",], "new_name")

# Rename object
# resp = kvp.rename_obj(["path","to","container"], "original_name.txt", "new_name.txt")

# Rename container
# resp = kvp.move_container(["path","to",], "original_name", "new_name")

if (resp is not None):
  if (incl_resp_body):
    print(resp.response_body)
  print("Server response: %s (%d bytes)" % (resp.status_code, len(resp.response_body)))
else:
  print("No operation performed")
