import os
from qiutil.logging import logger
from . import reader

def edit(*in_files, **opts):
    """
    Edits the given DICOM files. The *dest* option can be either the
    destination directory path or an output file namer function.
    If *dest* is a directory path, then the output file location is
    a file in the given destination directory with the same unqualified
    file name as the input file. If the *dest* option is a function,
    then the output file location is the result of calling that
    function with the input file path as an argument. The default is
    to edit the file in-place.

    :param in_files: the input DICOM files or directories containing
        DICOM files
    :param opts: the following options:
    :keyword dest: the destination directory or file namer function
    :yield: the :meth`qidicom.reader.next` pydicom dicom object
    """
    # Prepare the destination directory.
    dest = opts.get('dest')
    if dest:
        if isinstance(dest, str):
            dest = os.path.abspath(dest)
            if not os.path.exists(dest):
                os.makedirs(dest)
    else:
        dest = os.getcwd()

    # Open the DICOM store on each DICOM file (skipping non-DICOM files),
    # yield to the edit callback and save to the file in the destination
    # directory.
    for ds in reader.iter_dicom(*in_files):
        logger(__name__).debug("Editing the DICOM file %s..." % ds.filename)
        # Delegate the edit.
        yield ds
        # Make the output file name.
        if isinstance(dest, str):
            # The dest option is a parent directory.
            _, fname = os.path.split(ds.filename)
            out_file = os.path.join(dest, fname)
        else:
            # The dest option is a function.
            out_file = dest(ds.filename)
        # Save the modified dataset.
        ds.save_as(out_file)
        logger(__name__).debug("Saved the edited DICOM file as %s." % out_file)
