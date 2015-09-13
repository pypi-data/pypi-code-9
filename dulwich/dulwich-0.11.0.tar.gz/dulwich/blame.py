# blame.py -- Find what commit last modified a line
# Copyright (C) 2015 Jelmer Vernooij and others.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 2
# of the License or (at your option) a later version of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.

"""Find what commit last modified a line.
"""

def annotate_blob(store, final_commit, path):
    """Annotate the lines in a blob.

    :param store: Object store
    :param final_commit: Final commit SHA.
    :param path: Path in final commit
    :return: List of lines, as tuples with commit id, content
    """
    FIXME


def annotate_blob_commits(store, final_commit, path):
