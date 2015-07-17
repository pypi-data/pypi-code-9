# This file is part of Invenio.
# Copyright (C) 2014, 2015 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""Registry for WebSubmit."""

from flask_registry import ImportPathRegistry, RegistryProxy

from invenio.ext.registry import ModuleAutoDiscoverySubRegistry

websubmit = RegistryProxy(
    'websubmit', ImportPathRegistry,
    initial=['invenio.legacy.websubmit']
)

file_metadata_plugins = RegistryProxy('websubmit.file_metadata_plugins',
                                      ModuleAutoDiscoverySubRegistry,
                                      'file_metadata_plugins',
                                      registry_namespace=websubmit)
