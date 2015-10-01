import os

def str_remove_accents(s):
    """Utility to remove accents from characters in string"""
    
    import unicodedata
    return unicodedata.normalize('NFD', s).encode('ascii','ignore').decode('ascii')
    
def pdf_extract_text(path, pdfbox_path, pwd='', timeout=120):
    """Utility to use PDFBox from pdfbox.apache.org to extract Text from a PDF
    
    Parameters
    ----------
    path : str
        Path to source pdf-file
    pdfbox_path : str
        Path to pdfbox-app-x.y.z.jar
    pwd : str, optional
        Password for protected pdf files
    timeout : int, optional
        Seconds to wait for a result before raising an exception (defaults to 120).
    
    Returns
    -------
    file
        Writes the result as the name of the source file and appends '.txt'.
    
    Notes
    -----
    - Requires pdfbox-app-x.y.z.jar in a recent version (see http://pdfbox.apache.org).
    - Requires Java (JDK) 1.5 or newer (see http://www.oracle.com/technetwork/java/javase/downloads/index.html).
    - Requires java to be on the PATH.
    """
    
    if not os.path.isfile(path):
        raise IOError('path must be the location of the source pdf-file')
    
    if not os.path.isfile(pdfbox_path):
        raise IOError('pdfbox_path must be the location of the pdfbox.jar')
    
    import subprocess
    for p in os.environ['PATH'].split(':'):
        if os.path.isfile(os.path.join(p, 'java')):
            break
    else:
        print('java is not on the PATH')
        return
    try:
        if pwd == '':
            cmd = ['java', '-jar', pdfbox_path, 'ExtractText', path, path+'.txt']
        else:
            cmd = ['java', '-jar', pdfbox_path, 'ExtractText', '-password', pwd,
                path, path+'.txt']
        subprocess.check_call(cmd, stdin=subprocess.DEVNULL, 
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=timeout)
    
    except subprocess.TimeoutExpired as e:
        print('Timeout of {:.1f} min expired'.format(timeout/60))
    
    except subprocess.CalledProcessError as e:
        print('Text could not successfully be extracted.')