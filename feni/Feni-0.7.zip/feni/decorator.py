import os
import shutil
import yaml
import pathlib
import logging

def check_if_child(parent, child):
    if parent == child:
        return True
    for child_parent in child.parents:
        if child_parent == parent:
            return True
    return False

class Template:
    def __init__(self, template_file, embedd):
        self.file = template_file
        self.embedd = embedd

class Decorator:
    def __init__(self, folder_path, templates_folder, template_map):
        self.folder = folder_path
        self.template_folder = templates_folder
        self.file_handlers = {}
        with open(template_map, 'r') as f:
            self.template_configuration = yaml.load(f)
            
    def add_handler(self, extension, handler):
        self.file_handlers[extension] = handler

    def get_template_for_type(self, type):
        for template_file, configuration in self.template_configuration.items():
            if type in configuration['types']:
                return Template(template_file, configuration['embedd'] if 'embedd' in configuration else None)

    def build_decoration(self, target):
        logging.info("Buliding decoration")
        source_path = pathlib.PurePath(self.folder)
        templates_path = pathlib.PurePath(self.template_folder)
        if not os.path.isdir(target):
            os.mkdir(target)
        for dirinfo in os.walk(self.folder):
            for dir in dirinfo[1]:
                p = pathlib.PurePath(dirinfo[0], dir)
                if check_if_child(templates_path, p):
                    continue
                destination = os.path.join(target, str(p.relative_to(source_path)))
                if not os.path.isdir(destination):
                    os.mkdir(destination)
            for file in dirinfo[2]:
                p = pathlib.PurePath(dirinfo[0], file)
                if check_if_child(templates_path, p):
                    continue
                this_source = str(p)
                destination = os.path.join(target, str(p.relative_to(source_path)))
                if p.suffix in self.file_handlers:
                    handler = self.file_handlers[p.suffix]
                    handler.process_file(str(p), destination)
                else:
                    shutil.copyfile(this_source, destination)
