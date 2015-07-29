import sys
import os
import shutil
import fnmatch
import tempfile
import argparse
from io import StringIO

import pip

from . import config, __version__

MAIN_REPO = 'http://hg.code.sf.net/p/mimodd/source'


class MiModDInstallationError (Exception):
    pass


def find_executable(executable='mimodd', path=None, flags=os.X_OK):
    """Find the mimodd executable in the directories listed in 'path'.
 
    A string listing directories separated by 'os.pathsep'; defaults to
    os.environ['PATH'].  Returns the complete filename or None if not found.
    """
    if path is None:
        path = os.environ['PATH']
    paths = path.split(os.pathsep)
     
    if not os.path.isfile(executable):
        for p in paths:
            f = os.path.join(p, executable)
            if os.access(f, flags):
                return f
        return None
    else:
        return executable


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
             usage=argparse.SUPPRESS,
             formatter_class=argparse.RawDescriptionHelpFormatter,
             description = """

standard usage:

  MiModD.upgrade install     to upgrade to the latest available version
  
""")
    subparsers = parser.add_subparsers(title='available actions', metavar='')
    # upgrade install command
    p_install = subparsers.add_parser('install',
                help='upgrade your MiModD installation to a different release')
    p_install.add_argument('-v', '--version', default=argparse.SUPPRESS,
                help='the release number to upgrade to (default: latest)')
    p_install.set_defaults(pip_args=['install', 'MiModD{}'],
                           version_separator='==',
                           mode='install')
    # upgrade hg-install command
    p_hg_install = subparsers.add_parser('hg-install',
                help='upgrade to an unstable in-development version (NOT recommended for standard users)')
    p_hg_install.add_argument('-v', '--version', default=argparse.SUPPRESS, metavar='CHANGESET', help='the specific changeset to upgrade to (default: tip)')
    p_hg_install.set_defaults(pip_args=['install',
                                        'hg+'+MAIN_REPO+'{}#egg=MiModD'],
                              version_separator='@',
                              mode='hg-install')

    args = vars(parser.parse_args())
    # Logic of following argument parsing:
    # When used without args: run 'pip search MiModD' and display output.
    # When used with 'install' or 'hg-install' subcommand
    # and a specific version:
    # use 'pip install MiModD==version' or
    # 'pip install hg+MAIN_REPO@version#egg=MiModD'
    # to install that specific version.
    # For 'install' a check is performed first to see if the
    # user-provided version string is valid.
    # If no version is given, then for hg-install:
    # use 'pip install hg+MAIN_REPO#egg=MiModD'
    # to install the repository tip, but for install:
    # use 'pip install 'MiModD>current_version''
    # i.e., run upgrade only if a newer version than the currently
    # installed one is available.
    # Summary:
    # No restrictions apply when using hg-install, use at your own risk!
    # However, prevent the most annoying mistakes in install mode.
    if not args:
        print('Checking for latest available version ...')
        old_stdout = sys.stdout
        try:
            sys.stdout = buffer = StringIO()
            pip.main(['search', 'MiModD'])
        finally:
            sys.stdout = old_stdout
            print(buffer.getvalue())
    else:
        pip_args = args['pip_args']
        if 'version' in args:
            if args['mode'] == 'install':
                # Prevent downgrading beyond v0.1.5.3 when upgrading was
                # introduced.
                try:
                    new_version = tuple(int(d) for d in args['version'].split('.'))
                except:
                    print('Invalid version number.')
                    sys.exit(1)
                if new_version < (0, 1, 5, 3):
                    print('Cannot downgrade to versions older than 0.1.5.3')
                    sys.exit(1)
            pip_args[1] = pip_args[1].format(
                              args['version_separator']+args['version'])
        else:
            if args['mode'] == 'install':
                pip_args[1] = pip_args[1].format(
                                  '>'+str(__version__))
            else:
                pip_args[1] = pip_args[1].format('')
                
        warn_count = 0
        migrate_these = ['cfg.py']
        migrate_these_maybe = ['upgrade.py', 'enablegalaxy.py']
        current_package_dir = os.path.dirname(__file__)
        current_install_dir = os.path.dirname(current_package_dir)
        # check that we have write permissions in the current
        # installation directory. This check may be misleading since
        # it does not prove that we can delete things not owned by us,
        # but it is good enough in most cases.
        try:
            try:
                with tempfile.TemporaryFile(dir=current_install_dir):
                    pass
            except OSError:
                raise MiModDInstallationError(
                    'You do not seem to have permission to modify the current installation. Maybe you need to use "sudo"?')
            with tempfile.TemporaryDirectory(
                 prefix='MiModDinstall',
                 dir=config.tmpfiles_path) as temp_install_dir:
                temp_package_dir = os.path.join(temp_install_dir, 'MiModD')

                # pip install to temporary installation directory
                pip_args += ['--target', temp_install_dir]
                retcode = pip.main(pip_args)
                if retcode:
                    raise MiModDInstallationError(
                        'Installation error. Upgrade aborted')
                
                # migrate files to temporary package directory
                for f in migrate_these:
                    src = os.path.join(current_package_dir, f)
                    dst = os.path.join(temp_package_dir, f)
                    shutil.copyfile(src, dst)
                for f in migrate_these_maybe:
                    src = os.path.join(current_package_dir, f)
                    dst = os.path.join(temp_package_dir, f)
                    if not os.path.exists(dst):
                        shutil.copyfile(src, dst)

                # replace current package directory with temporary one
                try:
                    shutil.rmtree(current_package_dir)
                except OSError:
                    raise MiModDInstallationError(
                        'Cannot remove the current installation. Upgrade aborted')
                for d in os.listdir(current_install_dir):
                    p = os.path.join(current_install_dir, d)
                    if os.path.isdir(p) and fnmatch.fnmatch(d, 'MiModD-*-info'):
                        try:
                            shutil.rmtree(p)
                        except OSError:
                            print("""
WARNING: Failed to remove old installation info: {}.
Future runs of MiModD.upgrade may report a wrong installed version."""
                                  .format(d))
                            warn_count += 1
                for d in os.listdir(temp_install_dir):
                    src = os.path.join(temp_install_dir, d)
                    dst = os.path.join(current_install_dir, d)
                    if not os.path.exists(dst):
                        shutil.copytree(src, dst)
                
            try:
                # (re-)configure the Galaxy toolbox xml
                from . import enablegalaxy
                enablegalaxy.GalaxyAccess.set_toolbox_path()
            except:
                print("""
WARNING: Failed to migrate your Galaxy settings.
If you want to use your installation of MiModD with Galaxy, you will have to
run "python3 -m MiModD.enablegalaxy" to activate Galaxy support even if you
have already done so for your old installation.""")
                warn_count += 1

            # locate and upgrade the mimodd executable
            package_executable = os.path.join(current_package_dir,
                                              'bin', 'mimodd')
            if not os.path.isfile(package_executable):
                print("""
Script update FAILED! You will have to download the mimodd executable
separately and put it in a folder on your $PATH.""")
                warn_count += 1
            else:
                executable_update_success = False
                print()
                print('Trying to update mimodd executable ..')
                guess = find_executable()
                if guess:
                    if guess == package_executable:
                        # the new executable ended up on $PATH directly
                        # no action required
                        executable_update_success = True
                    else:
                        print('Found:', guess)
                        while True:
                            ans = input(
                                'Do you want to upgrade this file (y/n)? ')
                            if ans.upper() == 'Y':
                                try:
                                    shutil.copy(package_executable, guess)
                                except (IOError, OSError) as e:
                                    print(e.args)
                                else:
                                    executable_update_success = True
                                break
                            if ans.upper() == 'N':
                                break
                            print('Invalid choice:', ans)
                if executable_update_success:
                    print('new mimodd executable is at', guess)
                else:
                    print("""
FAILED to update the mimodd executable!
A copy of the new version can be found at {}.
To use mimodd from the command line, you can put a symbolic link to this file
into a folder on your $PATH. If you currently have an old copy of the script
in $PATH, the order of occurrence in $PATH determines which version takes
precedence and it may be best to remove the old file."""
                              .format(package_executable))
                    warn_count += 1
        except MiModDInstallationError as e:
            print(e.args[0])
            sys.exit(1)

        print()
        print('Upgrade completed! {} problem(s) encountered.'
              .format(warn_count or 'No'))
