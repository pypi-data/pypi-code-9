import hashlib
import zipfile

def sha256(filepath):
    """
        Function to calculate sha256 of a file in disk
        Params:
            - filepath (str): Path where the file is stored
        Return:
            - sha256 hash calculated
    """
    fd = open(filepath, 'rb')
    hasher_256 = hashlib.sha256()
    chunk = fd.read(1024)   
    while chunk:
        hasher_256.update(chunk)
        chunk = fd.read(1024)

    fd.close()
    return hasher_256.hexdigest()


def unpack(filepath, dst):
    """
        Function to generate a file from uncompressed file of an APK.
        Params:
            - filepath (str): Path where the APK is stored
            - dst (str): Path where the file generated will be saved.
        Return:
            - True is all was done.
            - False in case of error.
    """

    to_ret = True

    with open(filepath, 'rb') as fd:
        content = fd.read()

    try:
        zipped = zipfile.ZipFile(filename)
        for name in zipped.namelist():
            content += ' ' + zipped.read(name)

    except:
        to_ret = False

    with open(dst, 'wb') as fd:
        fd.write(content)
        
    return to_ret
