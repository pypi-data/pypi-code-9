""" mxODBC license settings for the mxODBC Zope DA.


    === LICENSE PROTECTION DEVICE =======================================

    WARNING: Unless you have written specific prior permissions from
    eGenix.com, any modification of the following code (either
    directly in the code or via a compile-time parameter) immediately
    causes a material breach of the eGenix.com Commercial License
    under which this code is made available to you, thereby making use
    of this Software illegal under the terms of the license!

    =====================================================================

"""
#
# IMPORTANT: Make sure that this file is *not* distributed in any way !!!
#

### Settings

MX_PRODUCT_ID = "mxODBC-for-Zope"
MX_PRODUCT_VERSION = "2.2"
MX_PRODUCT_KEY = "0x22e1e42afd7cf044ef3219c73959fa1592655a128e05d209da828f371d94636c8d65f7881049aa9d306aae81f54795bde1aa5d6b4a085acd7f8af045a1b832a12c13cd52626973a48050241f446bf84054a6b9493b2c154d13e6d5ed9739bff639e763835dd6279df231317145c5eb4ae703cde705c31c3a330a4f36c8a07b0290d6fb18319453ebc82c1d3164f798115e219b39fa77c54dfbf7db1bfcd0344344beece855e2f7f2f53a7627a303bd7468b38c9806e0ba6363d67feed0443ef8b56a26374e6f208b0a1ccd1a09a35a780062f0b625a0f4654d677a77a2bc60164e5652f41730c68b2f549f8f9622439bb7f71db658bcc6c26aded4ac83664941b"
MX_APPLICATION_KEY = "0xd"
MX_LICENSE_MODULE = "mxodbc_zopeda_license"

### Interface

import sys

# Setup common define_macros. These are currently mainly used for
# licensing customization.
def get_license_defines():

    defines = []

    # Setup the value formatting template
    if sys.platform[:3] == 'win':
        # Use escaped quotes that survive the VC++ command line
        # interface
        value_template = '\\"%s\\"'
    else:
        # Regular quotes for all other platforms
        value_template = '"%s"'

    # Convert global variables to defines
    settings = globals()
    for symbol_name in (
        'MX_PRODUCT_ID',
        'MX_PRODUCT_VERSION',
        'MX_PRODUCT_MODULE',
        'MX_PRODUCT_KEY',
        'MX_APPLICATION_KEY',
        'MX_LICENSE_MODULE',
        ):
        value = settings.get(symbol_name, None)
        if value is None:
            continue
        # Strip leading and trailing whitespace
        value = value.strip()
        if not value:
            continue
        # Remove quotes for the string values and requote depending on the
        # platform
        if ((value[0] == '"' and value[-1] == '"') or
            (value[0] == "'" and value[-1] == "'")):
            value = value[1:-1]
        value = value_template % value
        defines.append((symbol_name, value))

    return defines
