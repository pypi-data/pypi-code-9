# Copyright (c) 2014 IBM Corp.
# Copyright (c) 2015 NetApp, Inc. All Rights Reserved.

"""
Oslo's internationalization interface for the netapp-lib project
"""

import oslo_i18n

_translators = oslo_i18n.TranslatorFactory(domain='netapp-lib')

# The primary translation function using the well-known name "_"
_ = _translators.primary

# Translators for log levels.
#
# The abbreviated names are meant to reflect the usual use of a short
# name like '_'. The "L" is for "log" and the other letter comes from
# the level.
_LI = _translators.log_info
_LW = _translators.log_warning
_LE = _translators.log_error
_LC = _translators.log_critical
