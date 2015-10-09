import os
import re
from dicom import datadict
from qiutil.logging import logger
from qiutil import functions
from . import (reader, writer)

# Uncomment the following lines to debug pydicom.
# import dicom
# dicom.debug(True)


def select(ds, *tags):
    """
    Reads the given DICOM dataset tags.
    
    :param ds: the pydicom dicom object
    :param tags: the names of tags to read (default all unbracketed tags)
    :return: the tag name => value dictionary
    """
    if not tags:
        # Skip tags with a bracketed name.
        tags = (de.name for de in ds if de.name and de.name[0] != '[')
    tdict = {}
    for t in tags:
        try:
            # The tag attribute.
            attr = re.sub('\W', '', t)
            # Collect the tag value.
            tdict[t] = getattr(ds, attr)
        except AttributeError:
            pass

    return tdict


class Editor(object):
    """DICOM tag editor."""
    
    def __init__(self, **edits):
        """
        Creates a new DICOM tag editor.

        :param edits: the :attr:`edits` tag value modifications
        """
        self.edits = edits
        """
        The DICOM header (I{name}, I{value}) tag modifications. The *value*
        can be a literal or a function. If it is a function, then the
        function is called on the current tag value, e.g.::

            meta.Editor(PatientID='Subject001',
                        BodyPartExamined=str.upper)
        """

        # The VR used to create a new tag entry is the first member of the
        # pydicom datadict value for the tag object.
        self._tvr = {name: datadict.get_entry(self._tag_for(name))[0]
                     for name in self.edits}
        """The edit {tag: DICOM VR} dictionary."""

    def edit(self, dataset):
        """
        Applies this editor's :attr:`edits` tag value modifications.

        :param dataset: the pydicom dicom dataset object
        """

        # Set the tag values.
        for attr, value in self.edits.iteritems():
            if functions.is_function(value):
                # Apply a function to the current tag value.
                if hasattr(dataset, attr):
                    resolved = value(getattr(dataset, attr))
                    setattr(dataset, attr, resolved)
            elif hasattr(dataset, attr):
                setattr(dataset, attr, value)
            else:
                tag = self._tag_for(attr)
                dataset.add_new(tag, self._tvr[attr], value)

    def _tag_for(self, name):
        return datadict.tag_for_name(name)
