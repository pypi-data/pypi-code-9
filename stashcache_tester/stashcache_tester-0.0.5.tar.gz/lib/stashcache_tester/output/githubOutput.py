
import logging
import json
import time
import shutil
import os
from tempfile import NamedTemporaryFile

from stashcache_tester.output.generalOutput import GeneralOutput
from stashcache_tester.util.Configuration import get_option
from stashcache_tester.util.ExternalCommands import RunExternal


class GithubOutput(GeneralOutput):
    """
    
    :param dict sitesData: Dictionary described in :ref:`sitesData <sitesData-label>`.
    
    This class summarizes and uploads the download data to a github account.
    
    Github output requires an SSH key to be added to the github repository which is pointed to by the `repo` configuration option.
    
    Github output requires additional configuration options in the main configuration in the section `[github]`.  An example configuration could be::
    
        [github]
        repo = https://github.com/stashcache.github.io.git
        branch = master
        directory = data
        ssh_key = /home/user/.ssh/id_rsa
        
        
    The configuration is:
    
    repo
        The git repo to commit the data to.
        
    branch
        The branch to install repo.
        
    directory
        The directory to put the data summarized files into.
        
    ssh_key
        Path to SSH key to use when checking out and pushing to the repository.
        
    
    """
    
    git_ssh_contents = """#!/bin/sh
    
    exec ssh -i $SSH_KEY_FILE "$@"
    
    """
    
    def __init__(self, sitesData):
        GeneralOutput.__init__(self, sitesData)
        
        
    def _get_option(self, option, default = None):
        return get_option(option, section="github", default=default)
        
    
    def _summarize_data(self, sitesData):
        summarized = []
        
        # Average download time per site.
        for site in sitesData:
            cur = {}
            cur['name'] = site
            siteTimes = sitesData[site]
            total_runtime = 0
            for run in siteTimes:
                total_runtime += float(run['duration'])
            
            testsize = get_option("raw_testsize")
            if total_runtime = 0:
                cur['average'] = 0
            else:
                cur['average'] = (float(testsize*8) / (1024*1024)) / (total_runtime / len(siteTimes))
            
            summarized.append(cur)
            
        
        # Should we do violin plot?
        
        #summarized = sitesData 
        return summarized
        
    
    def startProcessing(self):
        """
        Begin summarizing the data.
        """
        
        summarized_data = self._summarize_data(self.sitesData)
        
        logging.debug("Creating temporary file for GIT_SSH")
        tmpfile = NamedTemporaryFile(delete=False)
        tmpfile.write(self.git_ssh_contents)
        git_sh_loc = tmpfile.name
        logging.debug("Wrote contents of git_ssh_contents to %s" % git_sh_loc)
        tmpfile.close()
        import stat
        os.chmod(git_sh_loc, stat.S_IXUSR | stat.S_IRUSR)
        os.environ["GIT_SSH"] = git_sh_loc
        
        # Download the git repo
        git_repo = self._get_option("repo")
        git_branch = self._get_option("branch")
        key_file = self._get_option("ssh_key")
        os.environ["SSH_KEY_FILE"] = key_file
        RunExternal("git clone --quiet --branch %s  git@github.com:%s output_git" % (git_branch, git_repo))
        
        # Write summarized data to new file
        output_dir = self._get_option("directory")
        output_filename = "%s.json" % time.strftime("%Y%m%d-%H%M%S")
        output_file = os.path.join("output_git", output_dir, output_filename)
        if os.path.exists(output_file):
            logging.error("Error, output file %s already exists!" % output_file)
            sys.exit(1)
        
        with open(output_file, 'w') as outfile:
            json.dump(summarized_data, outfile)
        
        # Write filename to index file
        index_filename = os.path.join("output_git", output_dir, "index.json")
        if not os.path.exists(index_filename):
            logging.error("Index file does not exist, bailing")
            sys.exit(1)
        with open(index_filename) as index_file:
            index = json.load(index_file)
        
        # Should we limit the size of 'files' to only ~30 files (30 days?)
        index['files'].append(output_filename)
        
        with open(index_filename, 'w') as index_file:
            json.dump(index, index_file)
        
        # Commit to git repo
        RunExternal("cd output_git; git add -f .")
        RunExternal("cd output_git; git commit -m \"Adding file %s\"" % output_filename)
        RunExternal("cd output_git; git push -fq origin %s" % git_branch)
        
        shutil.rmtree("output_git")
        
