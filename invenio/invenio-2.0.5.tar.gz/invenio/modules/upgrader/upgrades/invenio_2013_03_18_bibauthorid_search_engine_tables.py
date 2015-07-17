# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2013 CERN.
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

import warnings
from invenio.legacy.dbquery import run_sql

depends_on = ['invenio_release_1_1_0']

def info():
    return "Creates the bibauthorid search engine tables"

def do_upgrade():
    warnings.filterwarnings('ignore')
    run_sql("""CREATE TABLE IF NOT EXISTS `aidDENSEINDEX` (
                `name_id` INT( 10 ) NOT NULL,
                `person_name` VARCHAR( 256 ) NOT NULL,
                `personids` LONGBLOB NOT NULL,
                PRIMARY KEY (`name_id`)
               ) ENGINE=MyISAM""")

    run_sql("""CREATE TABLE IF NOT EXISTS `aidINVERTEDLISTS` (
                `qgram` VARCHAR( 4 ) NOT NULL,
                `inverted_list` LONGBLOB NOT NULL,
                `list_cardinality` INT( 10 ) NOT NULL,
                PRIMARY KEY (`qgram`)
               ) ENGINE=MyISAM""")

def estimate():
    return 1

