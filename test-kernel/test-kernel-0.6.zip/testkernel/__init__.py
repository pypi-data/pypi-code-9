def _is_root():
    """Checks if the user is rooted."""
    import ctypes, os
    try:
        return os.geteuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    return False

def cmdclass(path, user=None):
    """Build kernelspec cmdclass dict for the setuptools.setup method.

    Parameters
    ----------
    path: str
        Directory relative to the setup file that the kernel.json file lives in.
    user: [bool=None]
        Whether or not the nbextension should be installed in user mode.
        If this is undefined, the script will install as user mode IF the
        installer is not sudo.

    Usage
    -----
    For manual loading:
    # Assuming `./extension` is the relative path to the JS files.
    setup(
        name='testkernel',
        ...
        cmdclass=cmdclass('testkernel/data'),
    )
    """

    from setuptools.command.install import install
    from setuptools.command.develop import develop
    from os.path import dirname, abspath, join, exists, realpath
    from traceback import extract_stack
    from shutil import copytree, rmtree

    def get_ipython_dir():
        calling_file = extract_stack()[-2][0]
        return realpath(calling_file)

    try:
        # IPython/Jupyter 4.0
        # import jupyter_client
        from jupyter_client.kernelspec import install_kernel_spec
        from IPython.paths import get_ipython_dir
    except ImportError:
        # Pre-schism
        #from IPython.kernelspec import install_kernel_spec
        print ("ImportError install_kernel_spec")
  
    # Check if the user flag was set.
    if user is None:
        user = not _is_root()

    # Get the path of the extension
    calling_file = extract_stack()[-2][0]
    fullpath = realpath(calling_file)
    if not exists(fullpath):
        raise Exception('Could not find path of setup file.')
    source_dir = join(dirname(fullpath), path)
    profile_source_dir = join(source_dir,'profile_vpython')
    ipython_dir = get_ipython_dir()
    profile_destination_dir = join(ipython_dir,'profile_vpython')
    

    # Installs the kernel
    def run_kernel_install(develop):
        #jupyter_client.kernelspec.install_kernel_spec(source_dir, kernel_name='VPython', user=user)
        install_kernel_spec(source_dir, kernel_name='VPython', user=user)
        #install_kernel_spec(source_dir, kernel_name='VPython', user=user, replace=None, prefix=None)
        print (profile_source_dir)
        print (ipython_dir)
        print (profile_destination_dir)
        
        try:
            copytree(profile_source_dir, profile_destination_dir)
        except:
            rmtree(profile_destination_dir)
            copytree(profile_source_dir, profile_destination_dir)
        

    # Command used for standard installs
    class InstallCommand(install):
        def run(self):
            print("Installing Python module...")
            install.run(self)
            print("Installing custom kernel ...")
            run_kernel_install(False)

    # Command used for development installs (symlinks the JS)
    class DevelopCommand(develop):
        def run(self):
            print("Installing Python module...")
            develop.run(self)
            print("Installing custom kernel ...")
            run_kernel_install(True)

    return {
        'install': InstallCommand,
        'develop': DevelopCommand,
    }
