import os
import fnmatch
import functools

# Use the built-in version of scandir/walk if possible, otherwise
# use the scandir module version
try:
    from os import scandir, walk
except ImportError:
    from scandir import scandir, walk

class PatternFile:
    """Handler for files containing patterns"""

    # Default pattern directory
    PATTERN_DIR = os.path.join(os.getenv('HOME', './'), '.config/clean/')
    
    def __init__(self, name, allow_env = True, mode='r'):
        
        # Find the directory to store patterns
        if allow_env and 'CLEAN_PATTERN' in os.environ:
            config_dir = os.getenv('CLEAN_PATTERN')
        else:
            config_dir = self.PATTERN_DIR

        # Create the directory if he doesn't exist
        if not os.path.isdir(config_dir):
            os.makedirs(config_dir)

        # Append filename to config_dir
        self.fullpath = os.path.join(config_dir, name + '.ptrn')

        self.mode = mode


    def __iter__(self):
        """Iterator on the patterns stored in the pattern file"""

        # Create the file if he doesn't exist
        if not os.path.exists(self.fullpath):
            open(self.fullpath, 'a').close()
        
        # Read the file and yield each pattern
        with open(self.fullpath) as file:
            for pattern in file:
                yield pattern.strip()


    def __enter__(self):
        """Return file handler, opened with the mode given at initialisation"""

        self.file = open(self.fullpath, self.mode)
        return self.file


    def __exit__(self, type, value, traceback):
        self.file.close()

class CleaningFile:
    """Handler for a file being cleaned"""

    # Asking user
    prompt = 'Do your really want to remove {} ? '
    yes = ['yes', 'y']

    # Informing user
    removal_log = "{} has been removed"

    def __init__(self, fullpath, verbose=False, force=False):
        self.fullpath = fullpath
        self.verbose = verbose
        self.force = force

    def remove(self):
        """Remove the file"""

        # Has it been removed ?
        removed = False

        if not self.force:
            # Ask the user before removal
            if input(self.prompt.format(self.fullpath)).lower() in self.yes:
                os.remove(self.fullpath)
                removed = True
        else: # If self.force
            os.remove(self.fullpath)
            removed = True

        if self.verbose and removed:
            print(self.removal_log.format(self.fullpath))

class CleaningRequest:
    """Abstraction of a request using pattern matching"""

    def __init__(self, patterns, directories=None, recursive=False):
        self.patterns = patterns
        self.directories = directories
        self.recursive = recursive


    def recursive_request(self, directory):
        """recursive request"""

        rv = list()

        for root, dirs, files in walk(directory):

            # Function returning fullpath
            fullpath = lambda f: os.path.join(root, f)

            # matched files in current directory
            rv.extend(map(fullpath, self.match_files(files)))

        # if nothing in directory
        return rv


    def flat_request(self, directory):
        """flat request"""
        return self.match_files(os.listdir(directory))


    def __call__(self, directory, recursive=False):
        """dispatch request between recursive of flat"""
        if recursive:
            return self.recursive_request(directory)
        return self.flat_request(directory)


    def match_files(self, entities):
        """match set of files against patterns"""

        # entities is a set of non matched files
        entities = set(entities)

        for pattern in self.patterns:

            # match files against a single pattern
            matched_files = set(fnmatch.filter(entities, pattern))

            # remove matched files from entities
            entities = entities.symmetric_difference(matched_files)

            # yield each matched files
            yield from matched_files


    def __iter__(self):
        """Request using initialization values"""

        # Fail safe
        if not self.directories:
            self.directories = list()

        for directory in self.directories:
            for file in self(directory, self.recursive):
                yield file
