# -*- coding: utf-8 -*-
"""
    statico.tasks
    -------------
    Defines the tasks used by the 'statico' script
    :license: MIT, see LICENSE for more details.
"""
import os
import shutil
import feedparser
import jinja2 as jn
import datetime
from subprocess import call
from .utils import copy_directory, sorted_list_dir, get_gh_repos
from .helpers import process_files, process_index, process_atom_xml
from .pylog import ERROR, WARNING, SUCCESS, action
from .contents import FileManager, Article
from pathlib import Path


def new_item_task(klass, title):
    """
    Creates a new item
    :param klass: Page|Article  The type of the item
    :param title: str           The item's title
    :return:
    """
    settings = FileManager.get_settings()

    item = klass(title, settings.get('author', ''))
    result = item.create()

    if result is not None:
        print(SUCCESS + ' File created successfully.')
    else:
        print(ERROR + ' File not created.')

    return result


def generate_task(verbose=True):
    """
    Generates the site
    :param verbose: bool Verbose output
    """

    # Initialisation
    # --------------
    settings = FileManager.get_settings()
    templates_loader = jn.FileSystemLoader(os.path.join(os.getcwd(), 'templates'))
    templates_env = jn.Environment(loader=templates_loader)
    root_loader = jn.FileSystemLoader(os.getcwd())
    root_env = jn.Environment(loader=root_loader)

    # Get all filenames
    # -----------------
    page_files = sorted_list_dir(os.path.join('content', 'pages'))
    article_files = sorted_list_dir(os.path.join('content', 'articles'))
    articles = Article.get_articles(article_files)
    recent_articles = articles[:5]

    # Add GitHub repos
    # ----------------
    repos = get_gh_repos(settings.get('github_user'), settings.get('github_repo_count'))
    if not repos:
        print(ERROR + ' GitHub search repositories error. Check "github_user" in settings.json')

    # Create 'blog' and 'categories' directories
    # ------------------------------------------
    categories_dir = os.path.join('output', 'blog', 'categories')
    if not os.path.exists(categories_dir):
        os.makedirs(categories_dir)

    # Process pages and articles
    # --------------------------
    if verbose:
        print(action('Parsing articles and pages'))
    errors = process_files(
        page_files=page_files,
        article_files=article_files,
        recent_articles=recent_articles,
        templates_env=templates_env
    )
    if errors:
        print('\tErrors')
        print('\t------')
        print('\n'.join(['\t' + e for e in errors]))

    # Process index
    # -------------
    if verbose:
        print(action('Parsing index page'))
    error = process_index(
        articles=articles,
        recent_articles=recent_articles,
        repos=repos,
        settings=settings,
        templates_env=templates_env
    )
    if error is not None:
        print(ERROR + ' ' + error)

    # Process atom.xml
    # ----------------
    if verbose:
        print(action('Parsing atom.xml'))
    error = process_atom_xml(
        articles=articles,
        settings=settings,
        root_env=root_env
    )
    if error is not None:
        print(ERROR + ' ' + error)

    # Copy static directory
    # ---------------------
    if verbose:
        print(action('Generating static directory'))
    static = os.path.join('output', 'static')
    if os.path.exists(static):
        shutil.rmtree(static)
    error = copy_directory('static', os.path.join('output', 'static'))
    if error is not None:
        print(ERROR + ' ' + error)


def import_rss_task(url):
    """
    Import RSS
    :param url: str The RSS' url
    """
    rss = feedparser.parse(url)
    entries = rss.get('entries')

    FileManager.create_project()
    for entry in entries:
        item = Article(entry.get('title', ''), entry.get('author', ''), entry.get('updated').split('T')[0], 'html')
        content = entry.get('summary')
        item.create()
        item.get_file_pointer('a').write(content)


def isolate_task(partial_name):
    """
    Isolate articles for better regeneration performance
    :param partial_name: str The search string
    """
    articles_path = Path(os.path.join('content', 'articles'))
    at_least_one = False

    for article in articles_path.iterdir():
        if partial_name not in article.name:
            if not at_least_one:
                # Create stash directory if it doesn't exist
                stash_path = os.path.join('content', 'stash')
                if not os.path.exists(stash_path):
                    os.makedirs(stash_path)

            at_least_one = True
            print(article.name + ' -> ' + stash_path)
            shutil.move(str(article), stash_path)

    if not at_least_one:
        print(action('No articles matched'))


def integrate_task():
    """
    Integrate isolated items
    """
    stash = os.path.join('content', 'stash')

    if not os.path.exists(stash):
        print(WARNING + ' No stash directory found')
        return

    # Move all articles to content/articles
    print(action('Moving articles from stash'))
    stash_path = Path(stash)
    for article in stash_path.iterdir():
        shutil.move(str(article), os.path.join('content', 'articles'))

    # Remove stash directory
    print(action('Removing stash directory'))
    os.rmdir(stash)


def setup_gh_task(url):
    """
    Setup Github deployment
    :param url: str The remote url
    """
    print(action('cd output'))
    os.chdir('output')

    print(action('git init'))
    call(['git', 'init'])

    print(action('Add remote'))
    call(['git', 'remote', 'add', 'origin', url])


def gh_deploy_task():
    """
    Deploy via GH pages
    """
    print(action('cd output'))
    os.chdir('output')

    print(action('Pull changes'))
    call(['git', 'pull', 'origin', 'master'])

    print(action('Stage files'))
    call(['git', 'add', '--all', '.'])

    print(action('Commit files'))
    call(['git', 'commit', '-m', '"Site updated at ' + str(datetime.datetime.utcnow()) + ' UTC"'])

    print(action('Push changes to remote'))
    call(['git', 'push', 'origin', 'master'])

def rsync_deploy_task():
    """
    Deploy via rsync
    """
    settings = FileManager.get_settings()
    ssh_user = settings.get('rsync_ssh_user')
    document_root = settings.get('rsync_document_root')

    if not ssh_user or not document_root:
        print(ERROR + ' SSH user or document root not set in settings.json')
        return

    call('rsync -az --force --delete --progress -e "ssh -p22" ./output ' + ssh_user + ':' + document_root)
