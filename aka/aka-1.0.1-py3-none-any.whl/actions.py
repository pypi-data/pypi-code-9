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

import itertools
import collections
import shutil
import pathlib
import sys
import os

from aka.utils import (expand_stuff,
                       find_duplicates,
                       prompt_user)


def print_actions(actions):
    if actions:
        size = min(45, max(len(repr(action[0])) for action in actions))
        
        for old, new in actions:
            print("  {!s: <{}} -> {}".format(old, size, new))


EMERGENCY_PROMPT = """What should the program do?
retry    : try again (presumably you've fixed something in the meantime)
rollback : attempt to undo changes (except for the ones previously continue'd)
showroll : show which actions will be taken if you choose `rollback`
exit     : exit the program
continue : ignore the error and move on
> """

class Actions:
    def __init__(self, machine, basedir, temp_dir, pass_dirname=False, emergency_default=None):
        self.emergency_default = emergency_default
        self.basedir   = pathlib.Path(expand_stuff(basedir)).absolute().resolve()
        self.changed   = {}    # Files in `basedir` which are "selected" by `machine`
        self.unchanged = set() # The rest of the files in `basedir`
        self.actions   = []
        # ^ List of two-tuples, signifying actions, but only sublasses of Actions understands
        # how to use them. Note that RenameActions.make_action temporarily fills in triples,
        # but they are flattened later in RenameActions.__init__

        for old in self.basedir.iterdir():
            result = machine(old.name, str(old.parent)) if pass_dirname else machine(old.name)
            if result:
                normalized = self.basedir / pathlib.PurePath(expand_stuff(result))
                new = normalized.parent.resolve() / normalized.name

                if old == new:
                    self.unchanged.add(old)
                    continue # pointless to rename in this case
            
                self.changed[old] = new
                self.actions.append(
                    self.make_action(old, new, pathlib.Path(temp_dir)) # temp_dir can be a dummy value
                )
            else:
                self.unchanged.add(old)
        
        self.mapping = collections.defaultdict(dict) # Used for checking conflicts
        for old, new in self.changed.items():
            self.mapping[new.parent][old] = new
            
        self.continued_indices = set() # Keeping track of continued actions for smooth rollbacks

    def error(self, message, label="ERROR"):
        print("{}: {}".format(label, message), file=sys.stderr)

    def print_targets(self):
        print("Target directories:")
        for directory in self.mapping:
            print("  {}".format(directory))

    def find_conflicts(self):
        for directory in self.mapping:
                
            yield from self.conflicts_in_dir(
                directory,
                blacklist=self.make_blacklist(directory)
            )

            if not os.access(str(directory), os.X_OK | os.W_OK):
                yield "Target directory {} is not writable (and/or executable) by you!".format(directory)
                
    def report_conflicts(self):
        """
        Returns True if there are conflicts, False otherwise, and reports conflicts to the user as
        a side effect.
        """
        return bool([self.error(c) for c in self.find_conflicts()])
        
    def conflicts_in_dir(self, directory, blacklist):
        changes = self.mapping[directory]
        for old, new in changes.items():
            """
            `new` is the new name of the file, pointing into the dir in question.
            `blacklist` are "occupied" paths, obviously consisting of all the files
            in the dir in question, but it will omit files set for renaming.
            """
            if new in blacklist:
                yield "{} -> {} is a conflict!".format(old, new)
                
        dups = find_duplicates(changes.values())
        if dups:
            yield "There are duplicates among the new proposed names: {}".format(dups)
            
    def do_all(self, do_indices=None, rollback=False):
        """
        Returns False on failure, True on success.
        """
        if do_indices is None:
            do_indices = range(len(self.actions))
        
        for index in do_indices:
            while True:
                try:
                    (self.undo if rollback else self.do)(*self.actions[index])
                    break
                except Exception as error:
                    if rollback:
                        self.error("Error {} in rollback; ignoring and continuing".format(error))
                        break
                    else:
                        self.error(error, label="\n\nEMERGENCY MODE")
                        self.error("Error happened when trying to {} {} -> {}\n".format(self.verb, *self.actions[index]))
                        
                        rollbacks = tuple(idx for idx in reversed(range(index))
                                               if idx not in self.continued_indices)
                
                        tactic = (self.emergency_default or
                                  prompt_user(EMERGENCY_PROMPT, {"rollback", "exit", "continue", "retry"},
                                              callbacks={
                                                  "showroll": lambda: self.showroll(rollbacks)
                                              }, file=sys.stderr))
                        
                        if tactic == "rollback":
                            self.do_all(rollbacks, True)
                            return False
                        elif tactic == "continue":
                            self.continued_indices.add(index)
                            break # out of the while loop to move on to the next index
                        elif tactic == "retry":
                            continue # the while loop to try again
                        elif tactic == "exit":
                            return False # False means failure
                        
        # Failure if it had to continue an index (but a retry counts as a success)
        return not bool(self.continued_indices)



class RenameActions(Actions):
    verb = "rename"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # self.actions is now a list of triples, but I need them to be two-tuples.
        fst, snd = [], []
        self.simplified_actions = [] # for printing
        for old, temp, new in self.actions:
            fst.append( (old, temp) )
            snd.append( (temp, new) )
            self.simplified_actions.append( (old, new) )
            
        self.actions = fst + snd # Making sure the actions happens in the right order
        

    def showroll(self, rollbacks):
        print("Rollback actions:")
        print_actions([tuple(reversed(self.actions[idx])) for idx in rollbacks])

    def show_actions(self):
        print("Actions to be taken (simplified; doesn't show the temporary stage):")
        print_actions(self.simplified_actions)


    def do(self, old, new):
        print("Renaming {} -> {}".format(old, new))
        if new.exists():
            raise Exception("File {} already exists!".format(new))
        old.rename(new)
    
    def undo(self, old, new):
        print("Rollback renaming {} -> {}".format(new, old))
        if old.exists():
            raise Exception("File {} already exists!".format(new))
        new.rename(old)
        
    def make_action(self, old, new, temp_dir):
        return (old, temp_dir/old.name, new)
    
    def make_blacklist(self, directory):
        # In `basedir`, the changed files are "free" so to speak, for reusage
        return self.unchanged if directory == self.basedir else set(directory.iterdir())
    
    def conflicts_in_dir(self, directory, blacklist):
        yield from super().conflicts_in_dir(directory, blacklist)
        
        if any(parent in self.changed for parent in itertools.chain(directory.parents, [directory])):
               yield "Target dir {} (or any of its parents) is also about to be moved, that doesn't make sense".format(directory)
    

class CopyActions(Actions):
    verb = "copy"
    
    def showroll(self, rollbacks):
        print("Rollback actions:")
        for old, new in (self.actions[idx] for idx in rollbacks):
            print("  Delete {}".format(new))
            
    def show_actions(self):
        print("Actions to be taken:")
        print_actions(self.actions)


    def do(self, old, new):
        print("Copying {} -> {}".format(old, new))
        if new.exists():
            raise Exception("File {} already exists!".format(new))
        (shutil.copytree if old.is_dir() else shutil.copy2)(str(old), str(new))

    def undo(self, old, new):
        print("Removing {}".format(new))
        (shutil.rmtree if new.is_dir() else os.remove)(str(new))


    def make_action(self, old, new, temp_dir):
        return (old, new) # Doesn't need the temp_dir

    def make_blacklist(self, directory):
        return set(directory.iterdir())
