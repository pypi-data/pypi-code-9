#
# This file is part of the vecnet.emod package.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/vecnet.emod
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Functions to work with EMOD migration files
@TODO: move to vecnet.emod library (vecnet.emod.migration + command line script)

Please refer to
http://idmod.org/idmdoc/#DTKv1_6/v1_6FileFormatLayouts/Local Migration File.htm
for additional information about Local Migration File format

"Migration Blueprint" is a JSON file (or python dictionary) to present EMOD migration files in human-readable form


Example:
{
    "Metadata":
    {
        "IdReference": "vecnet.emod-nongeocoded",
        "Author": "Superuser"
    },
    "1": {
        "DestinationNodes": [2, 0, 0, 0, 0, 0, 0, 0],
        "MigrationRates": [3e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    "2": {
        "DestinationNodes": [1, 0, 0, 0, 0, 0, 0, 0],
        "MigrationRates": [3e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    }
}
In this case, migration file with two nodes will be created. Migration rate from node 1 to node 2 is 3e-5, and
migration rate from node 2 to node 1 is 3e-5

Metadata (optional) - Metadata section in Local Migration Metadata File (<Name>.bin.json). If not provided, library
defaults will be used.
Note that NodeCount in metadata will be overwritten by the library even if defined.
"""

import json
import struct
import sys
import datetime


def decompile_migration_blueprint(json_file, bin_file):
    """  Covert EMOD migration files (binary and metadata) to migration blueprint

    :returns: dict - Migration Blueprint
    """
    with open(json_file) as fp:
        metadata = json.load(fp)
    node_offsets = metadata["NodeOffsets"]
    blueprint = {}
    for i in range(len(node_offsets) / 16):
        node_id = int(node_offsets[i * 16:i * 16 + 8], 16)
        node_offset = int(node_offsets[i * 16 + 8:i * 16 + 16], 16)
        fp = open(bin_file, "rb")
        fp.seek(node_offset)
        destinations = fp.read(4 * 8)
        migration_rates = fp.read(8 * 8)
        fp.close()
        print struct.unpack("@dddddddd", migration_rates)
        node = {"NodeID": node_id,
                "DestinationNodes": struct.unpack("@iiiiiiii", destinations),
                "MigrationRates": struct.unpack("@dddddddd", migration_rates)}
        blueprint[node_id] = node
    return blueprint


def compile_migration_blueprint(blueprint, **metadata):
    """ Generate contents of migration metadata file and migration binary file
    !!! WARNING only local migration files are currently supported

    :returns (str) json file, (str) binary file
    """
    node_offsets = ""
    offset = 0
    bin_data = ""
    for node_id in blueprint:
        if node_id == "Metadata":
            # Not implemented yet
            pass
        node_offsets += "%0.8X%0.8X" % (int(node_id), offset)
        assert len(blueprint[node_id]["DestinationNodes"]) == 8
        assert len(blueprint[node_id]["MigrationRates"]) == 8
        bin_data += struct.pack("@iiiiiiii", *blueprint[node_id]["DestinationNodes"])
        bin_data += struct.pack("@dddddddd", *blueprint[node_id]["MigrationRates"])
        offset += 4 * 8 + 8 * 8

    metadata_file = {
        "Metadata":
            {
                "DateCreated": str(datetime.datetime.now()),
                "Tool": metadata["Tool"] if "Tool" in metadata else "vecnet.emod",
                "Author": metadata["Author"] if "Author" in metadata else "vecnet.emod",
                "IdReference": metadata["IdReference"] if "IdReference" in metadata else "vecnet.emod-nongeocoded",
                "NodeCount": len(blueprint),
                "DatavalueCount": 8
            },
        "NodeOffsets": node_offsets
        }
    return metadata_file, bin_data


def generate_migration_files(blueprint, json_filename, bin_filename, **metadata):
    """ Generate migration metadata file and migration binary file

    :param blueprint: Migration Blueprint (as a python dictionary)
    :type blueprint: dict
    :param json_filename: Filename of migration metadata file
    :type json_filename: str
    :param bin_filename: Filename of migration binary file
    :type bin_filename: str
    :param metadata: keyword arguments, additional metadata options (overwrite ones in Migration Blueprint)

    Usage example:
        generate_migration_files(migration_data_text,
                         "%s.bin.json" % filename_base,
                         "%s.bin" % filename_base,
                         **{"IdReference": "SR-nongeocoded"})
    """
    json_file, bin_file = compile_migration_blueprint(blueprint, **metadata)
    with open(json_filename, "wb") as fp:
        json.dump(json_file, fp, indent=4)
    with open(bin_filename, "wb") as fp:
        fp.write(bin_file)


if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename) as fp:
        migration_blueprint = json.load(fp)

    filename_base = filename.split(".json")[0]
    generate_migration_files(migration_blueprint,
                             "%s.bin.json" % filename_base,
                             "%s.bin" % filename_base)

    print "Successfully generated binary migration files"
