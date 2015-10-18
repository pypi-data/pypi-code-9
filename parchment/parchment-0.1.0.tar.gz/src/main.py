import os
from jinja2 import Environment, FileSystemLoader
from .read_file import File
from .generate import GenerateMarkdown
from .read_config import ReadConfig
from .helpers import *


def main():
    base_path = os.path.dirname(os.path.abspath('__file__'))
    cfg = ReadConfig(os.path.join(base_path, 'config.yaml'))

    env = Environment(loader=FileSystemLoader('templates'))
    index_template = env.get_template(cfg._config['theme'] + '/index.html')
    post_template = env.get_template(cfg._config['theme'] + '/post.html')

    # :list_file: list all the file names in directory `content`
    list_file = os.listdir(base_path + '/content/')
    list_file.sort(reverse=True)

    # :info_list: used to store all the infomartion that contains config info and posts info
    posts_info_list = []

    delete_file_folder(base_path+"/public")

    for file in list_file:

        # instance of File
        f = File(file)

        if not f.is_hidden_file():
            file_info_list = [f.year, f.month, f.day, f.title]
            full_path = base_path + "/public/" + "/".join(file_info_list)

            try:
                os.makedirs(full_path)
                os.mknod(full_path + '/index.html')
                print('creating directory public/{0}/{1}/{2}/{3}/index.html'.format(f.year, f.month, f.day, f.title))
            except FileExistsError:
                delete_file_folder(full_path)
                os.makedirs(full_path)
                os.mknod(full_path + '/index.html')
                print('File exists')

            with open(base_path + '/content/' + file, 'r') as markdown_file:
                md_f = markdown_file.read()
                generate_markdown = GenerateMarkdown(md_f)
            posts_dict = {}
            posts_dict['title'] = f.title
            posts_dict['body'] = generate_markdown.output
            posts_dict['src'] = os.path.join(f.year, f.month, f.day, f.title, 'index.html')
            posts_info_list.append(posts_dict)

            keys_list = cfg.get_config_keys()
            for key in keys_list:
                cfg.key = cfg._config[key]

            output_post_template = post_template.render(post=posts_dict, _=cfg._config)

            with open(full_path + '/index.html', 'w+') as output_post_file:
                output_post_file.write(output_post_template)

    '''
        copy folders from parchment/templates/yourtheme/ to /parchment/public/
    '''
    cp_folders(os.path.join(base_path, 'templates', cfg._config['theme']), os.path.join(base_path, 'public'))

    output_index_template = index_template.render(posts=posts_info_list, _=cfg._config)
    with open(base_path + '/public/' + 'index.html', 'w+') as output_index_file:
        output_index_file.write(output_index_template)
