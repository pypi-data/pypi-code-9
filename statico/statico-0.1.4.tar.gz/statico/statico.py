# -*- coding: utf-8 -*-

__version__ = '0.1.4'
__author__ = 'Ossama Edbali (ossedb@gmail.com)'


import sys
import os
import argparse as ap
from colorama import Fore, Back, Style
from livereload import Server, shell
from .contents import FileManager, Article, Page
from .tasks import generate_task, new_item_task, import_rss_task,\
    rsync_deploy_task, isolate_task, integrate_task, setup_gh_task, gh_deploy_task


def run_server():
    root = os.path.abspath('output')
    server = Server()
    server.watch(root)
    server.serve(port=8000, host='localhost', root=root)


def run():

    # Create project
    # --------------
    if len(sys.argv) == 1:
        if os.path.isfile('.statico'):
            print('\n' + Fore.BLACK + Back.YELLOW + 'WARNING' +
                  Fore.RESET + Back.RESET + ' This directory is already a "statico" project.\n')
            return

        print('\n==== CREATE SITE ====\n')
        FileManager.create_project()
        return

    # Argument definition
    # -------------------
    parser = ap.ArgumentParser()
    parser.add_argument(
        '-g', '--generate', help='Generate the output directory to upload to the web server', action='store_true'
    )
    parser.add_argument(
        '-p', '--page', help='Create a page', type=str
    )
    parser.add_argument(
        '-a', '--article', help='Create an article', type=str
    )
    parser.add_argument(
        '-c', '--clear', help='Clear directory', action='store_true'
    )
    parser.add_argument(
        '-P', '--preview', help='Preview your site', action='store_true'
    )
    parser.add_argument(
        '-r', '--rss', help='Import Atom RSS feed', type=str
    )
    parser.add_argument(
        '-s', '--setup-gh-deploy', help='Setup GitHub Pages deployment', action='store_true'
    )
    parser.add_argument(
        '-d', '--gh-deploy', help='Deploy to GitHub Pages', action='store_true'
    )
    parser.add_argument(
        '-R', '--rsync-deploy', help='Deploy with rsync', action='store_true'
    )
    parser.add_argument(
        '-i', '--isolate', help='Isolate an article', type=str
    )
    parser.add_argument(
        '-I', '--integrate', help='Integrate article changes', action='store_true'
    )
    args = parser.parse_args()

    if not os.path.isfile('.statico') and not args.rss:
        print('\n' + Fore.BLACK + Back.YELLOW + 'WARNING' +
              Fore.RESET + Back.RESET + ' This is not a "statico" directory. Run "statico" to mark it as so.\n')
        return

    # Commands matching
    # =================
    if args.generate:
        print('\n==== GENERATE SITE ====\n')
        generate_task()
        print(
            'Head to "output" to view your generated site.\n'
            'Now you are ready to upload your site.\n'
            'Type ' + Fore.WHITE + Back.GREEN + Style.BRIGHT + 'statico --preview'
            + Fore.RESET + Back.RESET + Style.RESET_ALL + ' to get a preview of your site.'
        )
    elif args.page:
        new_item_task(Page, args.page)
    elif args.article:
        new_item_task(Article, args.article)
    elif args.clear:
        if input('\nAre you sure you want to clear the workspace? [y/n] ').lower() in ['y', 'yes']:
            FileManager.clear_workspace()
    elif args.preview:
        print('\n==== PREVIEW ====\n')
        run_server()
    elif args.rss:
        print('\n==== RSS IMPORT TASK ====\n')
        import_rss_task(args.rss)
    elif args.setup_gh_deploy:
        print('\n==== SETUP GH TASK ====\n')
        url = input('Please enter your Github endpoint url: ')
        setup_gh_task(url)
    elif args.gh_deploy:
        print('\n==== GH DEPLOY TASK ====\n')
        gh_deploy_task()
    elif args.rsync_deploy:
        rsync_deploy_task()
    elif args.isolate:
        print('\n==== ISOLATE ARTICLES ====\n')
        isolate_task(args.isolate)
    elif args.integrate:
        print('\n==== INTEGRATE ARTICLES ====\n')
        integrate_task()

    print(Fore.RESET + Back.RESET + Style.RESET_ALL)
