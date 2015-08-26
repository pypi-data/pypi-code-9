#    Copyright 2014, Cisco Systems.

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
""" Exceptions class for ucswrapper module for Cisco UCS Python UcsSdk."""

class UcsWrapperException(BaseException):
    """ Parent class for all ucswrapper exceptions. """
    message = 'UCS Exception occured'
    def __init__(self, message):
        super(UcsWrapperException, self).__init__(message)
    pass


class UcsLoginError(UcsWrapperException):
    """LoginFailure Error"""
    message = 'Authentication failed'

    def __init__(self, message):
        super(UcsLoginError, self).__init__(message)


class UcsConnectionError(UcsWrapperException):
    """ Cannot connect to UCS Manager. """
    def __init__(self, message, error):
        message = 'Service unavailable, failed with error: %(error)s'
        super(UcsConnectionError, self).__init__(message)

class UcsOperationError(UcsWrapperException):
    """ Configuration Error. """
    def __init__(self, operation, error):
        message = _("%(operation)s failed, error: %(error)s")
        super(UcsOperationError, self).__init__(message)
