import os
import re
import shutil

import simpress.logger
import simpress.web
from simpress.logger import logger


def build():
    deploy_dir = '_deploy'
    truncate_deploy_dir(deploy_dir)
    copy_static_files(os.getcwd(), deploy_dir)
    [build_page(x, deploy_dir) for x in find_pages(os.getcwd())]


def truncate_deploy_dir(deploy_dir):
    if os.path.exists(deploy_dir):
        logger().info('truncate deploy dir "%s"' % deploy_dir)
        shutil.rmtree(deploy_dir)


def copy_static_files(src, dst):
    logger().info('copy static files')
    shutil.copytree(
        src, dst,
        ignore=shutil.ignore_patterns('_*', '*.md', '*.py'))


def build_page(url, deploy_dir):
    filename = os.path.join(deploy_dir, url)
    _ensure_dir(filename)
    html = simpress.web.create_app().test_client().get(
        url, follow_redirects=True).data.decode('utf-8')
    logger().info('build %s (%dbytes)' % (url, len(html)))
    with open(filename, 'w') as f:
        f.write(html)


def _ensure_dir(filename):
    dirname = os.path.dirname(filename)
    if dirname and not os.path.isdir(dirname):
        os.makedirs(dirname)


def find_pages(pages_dir):
    pages = []
    for (root, dirs, files) in os.walk(pages_dir):
        path = root.replace(pages_dir, '', 1)
        pages.extend([
            os.path.join(path, f).lstrip('/') for f in files
            if re.search(r'\.md$', f)])
    return sorted(
        [re.sub(r'\.md$', '.html', x) for x in pages])
