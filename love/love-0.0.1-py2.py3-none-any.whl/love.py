# -*- coding: utf-8 -*-

import emoji
import os
import sys
import random
import getpass
import difflib
import subprocess
import webbrowser

import pkgtools.pypi as pp
import github
from travispy import TravisPy

from time import sleep
# from cookiecutter.main import generate_context, generate_files

import keyring


import logging

heart = """
    oo                                        
       oo     OOOOOOOO:       OOOOOOOO!       
          oOOOO!!!!;;;;O    OO.......:;!O     
         'OOO!!!;;;;;;;;O  O.......:   ;!O    
         OOO!!!!;;::::::.OO........:    ;!O   
         OO!!!!;;:::::..............:   ;!O   
         OOO!!!;::::::..............:   ;!O   
          OO!!;;::::::.............:   ;!O           Made With Love
           OO!;;::::::......oo.....::::!O     
             O!!;::::::........oo..:::O                  - M - 
               !!!;:::::..........ooO         
                  !!;:::::.......O   oo       
                    ;;::::.....O        oo  ,o
                       :::..O              ooo
                         ::.              oooo
                          :                   
"""

from colored import fg, bg, attr

cheart = "%s%s%s" %(fg('deep_pink_3b'),heart, attr(0))





GITHUB_NEW_TOKEN_URI = 'https://github.com/settings/tokens/new'

try:
    import curses
except ImportError:
    curses = None

def _stderr_supports_color():
    color = False
    if curses and hasattr(sys.stderr, 'isatty') and sys.stderr.isatty():
        try:
            curses.setupterm()
            if curses.tigetnum("colors") > 0:
                color = True
        except Exception:
            pass
    return color



emoji_level = {
        10:emoji.emojize(":broken_heart:"),
        20:emoji.emojize(":growing_heart:"),
        30:emoji.emojize(":heart_with_arrow:")
}


class LogFormatter(logging.Formatter):
    """Log formatter with colour support
    """
    DEFAULT_COLORS = {
        logging.INFO: 2, # Green
        logging.WARNING: 3, # Yellow
        logging.ERROR: 1, # Red
        logging.CRITICAL: 1,
    }

    def __init__(self, color=True, datefmt=None):
        r"""
        :arg bool color: Enables color support.
        :arg string fmt: Log message format.
        It will be applied to the attributes dict of log records. The
        text between ``%(color)s`` and ``%(end_color)s`` will be colored
        depending on the level if color support is on.
        :arg dict colors: color mappings from logging level to terminal color
        code
        :arg string datefmt: Datetime format.
        Used for formatting ``(asctime)`` placeholder in ``prefix_fmt``.
        .. versionchanged:: 3.2
        Added ``fmt`` and ``datefmt`` arguments.
        """
        logging.Formatter.__init__(self, datefmt=datefmt)
        self._colors = {}
        if color and _stderr_supports_color():
            fg_color = (curses.tigetstr("setaf") or
                        curses.tigetstr("setf") or "")
            if (3, 0) < sys.version_info < (3, 2, 3):
                fg_color = str(fg_color, "ascii")

            for levelno, code in self.DEFAULT_COLORS.items():
                self._colors[levelno] = str(curses.tparm(fg_color, code), "ascii")
            self._normal = str(curses.tigetstr("sgr0"), "ascii")

            scr = curses.initscr()
            self.termwidth = scr.getmaxyx()[1]
            curses.endwin()
        else:
            self._normal = ''
            # Default width is usually 80, but too wide is worse than too narrow
            self.termwidth = 70

    def formatMessage(self, record):
        right_text = '{initial}-{name}'.format(initial=record.levelname[0],
                                               name=record.name)
        if record.levelno in self._colors:
            start_color = self._colors[record.levelno]
            end_color = self._normal
        else:
            start_color = end_color = ''
        emo = emoji_level[record.levelno]


        return emo +' '+start_color + '[' +right_text + '] ' +  record.message + end_color + ' '+emo





def main(proposal=None, target_dir=None):
    """
    completly set-up a package in the target dir (using cookie cutter) 
        

    """
    print(cheart)
    log = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setFormatter(LogFormatter())
    logging.root.addHandler(handler)
    logging.root.setLevel(20)
    log.setLevel(20)

    log.info("INFO TEST")
    log.warn("WARN TEST")

    if not target_dir:
        target_dir = os.getcwd()
        log.info('will use target dir : %s', target_dir)

    token = keyring.get_password('session','github_token')

    if token is None:
        GITHUB_NEW_TOKEN_URI = 'https://github.com/settings/tokens/new'
        log.info(emoji.emojize(":heart_with_arrow: == LOVE == :heart_with_arrow:"))
        log.info("I will need a new token to access your GitHub account, please give me a token that have `write:repo_hook` enable.")
        log.info("I'll try to open github for you at the right page, otherwise please visit %s", GITHUB_NEW_TOKEN_URI)
        sleep(5)
        webbrowser.open_new_tab(GITHUB_NEW_TOKEN_URI)
        token = getpass.getpass('github token:')
        keyring.set_password('session','github_token', token)
        log.info('token stored in your keyring as session:github_token')


    # generate a python package name

    adjectives = ['red','green','blue','purple','fluffy','soft','hard','golden','silver', 'pathetic', 'intrepid', 'jovial' , 'long']
    nouns = ['moon', 'frog', 'lake','orchid','sapphire','gem','sun','lily','ocean','lampshade','fish', 'koala', 'shark', 'kangaroo']
    if proposal and not proposal.isidentifier() and len(proposal)>3:
        log.info('package names should be valid python identifiers, and at least 3 letters long : %s', proposal)
        sys.exit(-1)


    if not proposal:
        proposal = random.choice(adjectives).capitalize()+random.choice(nouns).capitalize()
    plist = None

    #  compare name with existing package name, warn if too close

    log.info('Comparing "%s" to other existing package names...' % proposal)
    pypi = pp.PyPIXmlRpc()
    # cache that on a weekly basis ?
    if plist is None:
        plist = pypi.list_packages()
    closest = difflib.get_close_matches(proposal.lower(), map(str.lower, plist), cutoff=0.8)
    if closest:
        if proposal in closest:
            log.error(proposal, 'already exists, maybe you would prefer to contribute to this package?')
        else:
            log.warn('%s name is close to the following package name: %s', proposal,  closest)
    else:

        log.info('"%s" seems to have a sufficiently specific name, continuing...', proposal)


    #  Actually authenticate with github 
    #  Create (if do not exist) the named repo, and and clone URL.

    gh = github.Github(token)
    user = gh.get_user()
    log.info('Logged in on GitHub as %s ', user.name)
    from github import UnknownObjectException 
    try:
        repo = user.get_repo(proposal)
        log.info('It appears like %s repository already exists, using it as remote', proposal)
    except UnknownObjectException:
        repo = user.create_repo(proposal)

    ssh_url = repo.ssh_url
    slug = repo.full_name
    log.info('Working with repository %s', slug)


    # Clone github repo locally, over SSH an chdir into it

    log.info("Cloning github repository locally")
    log.info("Calling subprocess : %s", ' '.join(['git', 'clone' , ssh_url]))
    subprocess.call(['git', 'clone' , ssh_url])
    os.chdir(proposal)
    log.debug('I am now in %s', os.getcwd())

    repo, user = enable_travis(token, slug, log) 
    project_layout(proposal, user, repo, log)
    packaging_init(log)


# insert travis here. 

def enable_travis(token, slug, log):
    """
    Enable Travis automatically for the given repo.

    this need to have access to the GitHub token.
    """

    # Done with github directly. Login to travis

    travis = TravisPy.github_auth(token, uri='https://api.travis-ci.org')
    user = travis.user()
    log.info('============= Configuring Travis.... ===========')
    log.info('Travis user: %s', user.name)

    # Ask travis to sync with github, try to fetch created repo with exponentially decaying time.

    last_sync = user.synced_at
    log.info('syncing Travis with Github, this can take a while...')
    repo = travis._session.post(travis._session.uri+'/users/sync')
    import time
    for i in range(10):
        try:
            time.sleep((1.5)**i)
            repo = travis.repo(slug)
            if travis.user().synced_at == last_sync:
                raise ValueError('synced not really done, travis.repo() can be a duplicate')
            log.info('\nsyncing done')
            break
        # TODO: find the right exception here
        except Exception:
            pass
    ## todo , warn if not found


    #  Enable travis hook for this repository

    log.info('Enabling Travis-CI hook for this repository')
    resp = travis._session.put(travis._session.uri+"/hooks/",
                        json={
                            "hook": {
                                "id": repo.id ,
                                "active": True
                            }
                        },
                      )
    if resp.json()['result'] is True:
        log.info('Travis hook for this repository is now enabled.')
        log.info('Continuous integration test should be triggered every time you push code to github')
    else:
        log.info("I was not able to set up Travis hooks... something went wrong.")

    log.info('========== Done configuring Travis.... =========')
    return repo, user

def codecov():
    pass

def coveralls():
    # ##  Do the same for read the doc.

    # ## Shoudl we do https://coveralls.io/?

    # ## Todo
    #     - initiate template with something like cookie cutter
    #     - handle case where use is not registered with one of the above services.
    #     - easier way to get github token
    pass

def project_layout(proposal, user, repo, log):
    """
    generate the project template

    proposal is the name of the project, 
    user is an object containing some information about the user. 
        - full name, 
        - github username
        - email



    """

    proposal = proposal.lower()

    #context_file = os.path.expanduser('~/.cookiecutters/cookiecutter-pypackage/cookiecutter.json')
    #context = generate_context(context_file)

    # os.chdir('..')
    # context['cookiecutter']['full_name'] = user.name
    # context['cookiecutter']['email'] = user.email
    # context['cookiecutter']['github_username'] = user.login
    # context['cookiecutter']['project_name'] = proposal
    # context['cookiecutter']['repo_name'] = proposal.lower()


    os.mkdir(proposal)
    with open( '/'.join([proposal, '__init__.py']), 'w') as f: 
        f.write("""
        
        __version__ = '0.0.1'

        """)

    #generate_files(
    #        repo_dir=os.path.expanduser('~/.cookiecutters/cookiecutter-pypackage/'),
    #        context=context
    #    )

    log.info('Workig in %s', os.getcwd())
    os.listdir('.')

    subprocess.call(['git','add','.'])

    subprocess.call(['git','commit',"-am'initial commit of %s'" % proposal])

    subprocess.call(['git', "push", "origin", "master:master"])

    #webbrowser.open('https://travis-ci.org/{slug}'.format(slug=repo.slug))

def packaging_init(log):
    log.info('======= Setting up packaging with flit =========')
    log.info('Please answer the following questions: ')
    from flit.init import TerminalIniter
    TerminalIniter().initialise()
    log.info('======= Done Setting up packaging ==============')

