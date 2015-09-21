#!/usr/bin/env python

from __future__ import print_function

import sys
import os
import ntpath
import subprocess
from click import confirm
from shutil import copytree

from os.path import join, exists, expanduser

class Page():
    def __init__(self, args):
        self.page_dir = args['page_dir']
        self.editor = args['editor']

        if not exists(self.page_dir):
            import minpages
            data_dir = join(minpages.__path__[0],'pages')
            if confirm(
"""Page directory not yet created at '{page_dir}'.
Would you like to create it from {data_dir}?""".format(
                    page_dir=self.page_dir,
                    data_dir=data_dir
            )):
                copytree(data_dir,self.page_dir)
            else:
                sys.exit("No page directory, halted")


        if args['page'] is None:
            self.show_all_pages()
        elif args['edit']:
            self.edit_page(args['page'])
        elif args['delete']:
            self.delete_page(args['page'])
        else:
            self.show_page(args['page'])
       
    def show_all_pages(self):
        files = os.listdir(self.page_dir)
        print('Pages: ')
        print('-'*50)
        for file_name in files:
            if not(file_name[0] == '.'):
                print(ntpath.basename(file_name))
        print('-'*50)
    def show_page(self, page):
        file_name = join(self.page_dir, page)
        if exists(file_name):
            print(page+':')
            print('-'*50)
            with open(file_name,'r') as fout:
                print(fout.read())
            print('-'*50)
        else:
            print("Page '"+page+"' does not exist")
            if confirm("Would you like to create it?"):
                self.edit_page(page)
    def edit_page(self, page):
        file_name = join(self.page_dir, page)
        try:
            subprocess.call([self.editor, file_name])
        except OSError:
            print("Editor: '"+self.editor+"' does not exist",\
                    file=sys.stderr)
        self.show_page(page)
    def delete_page(self, page):
        file_name = join(self.page_dir, page)
        if exists(file_name):
            if confirm(\
                    "Are you sure you want to delete the page '"\
                    + page + "'?" ):
                os.remove(file_name)
                print("Removed page")
            else:
                print("Did not remove page")
        else:
            print("Page '"+page+"' does not exist")


