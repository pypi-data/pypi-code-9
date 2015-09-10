"""
Copyright (C) 2015 Mattias Ugelvik
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import pathlib
import sys

from aka.utils import temporary_directory, yes_no_prompt, expand_stuff
from aka.actions import RenameActions, CopyActions



RENAME_PROMPT = """
The files will be renamed as shown above (in two passes though, in order to avoid
collisions). This program searched for name conflicts in all target directories
and did not find any. If errors do pop up, you'll be taken to an emergency mode
where you can roll back changes. Continue?"""

COPY_PROMPT = """
The files will be copied as shown above. This program searched for name conflicts
in all target directories and did not find any. If errors do pop up, you'll be taken
to an emergency mode where you can roll back changes. Continue?"""
        

def perform_actions(machine, location, prompt, emergency, pass_dirname,
                    action_class, prompt_text, temp_dir="/dummy"):
    assert emergency in {None, "continue", "rollback", "exit"}

    actions = action_class(machine, location, temp_dir, pass_dirname, emergency)
    
    if not actions.actions:
        print("No files to {}".format(actions.verb))
        return True
    elif not actions.report_conflicts():
        if not prompt:
            return actions.do_all()
        
        else:
            actions.show_actions()
            actions.print_targets()
            if yes_no_prompt(prompt_text, default=False):
                return actions.do_all()
    else:
        print("Aborting...", file=sys.stderr)
        return False

def rename(machine, location=".", prompt=True, emergency=None, pass_dirname=False):
    """
    Renames files in the directory `location`, returning True on success, False
    if problems are detected (like naming conflicts). It can also return False if
    emergency mode is entered and the user selects "exit" ,"rollback" or "continue"
    (although not "retry"; that is considered a success).

    Every filename will be passed to the callable `machine` which should give the
    new name for the given file. If `machine` returns a falsy value then the
    filename will be ignored (i.e., not renamed). If `dirname` then `machine` will
    be called with `machine(fn, dirname)` where `fn` is the filename as usual and
    where `dirname` is the absolute path to the directory in which `fn` is located.

    The filename `machine` returns can point outside of `location`, in which
    case the file will be moved. If it's a relative path, it will be relative with
    respect to `location`.

    A prompt will appear asking the user whether `rename` should proceed if `prompt`
    is truthy.

    `emergency` specifies which action to be taken in case of an emergency.
    By default it will query the user, but you can set it to "rollback" or "continue"
    or "exit".
    
    If an error occurs in the process of renaming, then you will be put in emergency
    mode where you can rollback changes; continue; exit the program; or retry.
    
    If you choose "continue" or "exit" in emergency mode then some files will be left
    behind in the temporary directory; the location of this directory will be printed
    before exit.
    """
    with temporary_directory() as temp_dir:
        return perform_actions(machine, location, prompt, emergency, pass_dirname,
                               RenameActions, RENAME_PROMPT, temp_dir)

def copy(machine, location=".", prompt=True, emergency=None, pass_dirname=False):
    """
    Like `aka.rename`, but copies files instead. 
    """
    return perform_actions(machine, location, prompt, emergency,
                           pass_dirname, CopyActions, COPY_PROMPT)
