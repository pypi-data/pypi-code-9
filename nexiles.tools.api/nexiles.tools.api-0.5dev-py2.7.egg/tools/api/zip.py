from zipfile import ZipFile
import os
import logging
logger = logging.getLogger("nexiles.tools.api")


def unzip(zip_file):
    """unzip ()

    Unpack the app zip to the source directory.
    If we find a diretory, we create it.

    Because of #22 we have to build the folder
    structure to unzip the template app propper
    on windows.

    :param zip_file:   the app zip file we load from windchill
    """
    zip_file = "build/"+zip_file
    try:
        zip = ZipFile(zip_file)
        for file in zip.namelist():
            if file.endswith('/'):
                os.makedirs(file)  # Creates a directory.
            else:
                zip.extract(file)  # Extracts a file.
        logger.info('Created the app successfully')
    except Exception, e:
        logger.error("While creating the app an error occurred: ", e)

