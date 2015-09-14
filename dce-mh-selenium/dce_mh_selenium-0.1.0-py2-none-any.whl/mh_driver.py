#!/usr/bin/env python
from time import sleep

import click
from fabric.context_managers import cd
from selenium.common.exceptions import TimeoutException

click.disable_unicode_literals_warning = True

from unipath import Path
from fabric.api import run, abort, env, hide, sudo
from fabric.operations import put
from fabric.colors import cyan
from fabric.contrib.files import exists as remote_exists

from mh_selenium.utils import selenium_options, inbox_options, pass_state, \
    init_driver, base_url_arg, init_fabric
from mh_selenium.pages import RecordingsPage, AdminPage, TrimPage, \
                              UploadPage

@click.group()
def cli():
    pass

@cli.command()
@click.option('--presenter')
@click.option('--presentation')
@click.option('--combined')
@click.option('-i', '--inbox', is_flag=True)
@click.option('--live_stream', is_flag=True)
@selenium_options
@pass_state
@init_driver('/admin')
def upload(state, presenter, presentation, combined, inbox, live_stream):

    page = RecordingsPage(state.driver)
    page.upload_recording_button.click()

    page = UploadPage(state.driver)
    page.enter_text(page.title_input, "My Test Upload")
    page.enter_text(page.type_input, "L01")
    page.set_upload_files(presenter=presenter,
                          presentation=presentation,
                          combined=combined,
                          is_inbox=inbox)
    page.workflow_select.select_by_value('DCE-production')
    page.set_live_stream(live_stream)
    page.set_multitrack(combined is not None)
    page.upload_button.click()
    page.wait_for_upload_finish()

@cli.command()
@click.option('-f', '--filter')
@click.option('-c', '--count', type=int, default=None)
@selenium_options
@pass_state
@init_driver('/admin')
def trim(state, filter=None, count=None):

    page = AdminPage(state.driver)
    page.recordings_tab.click()
    page = RecordingsPage(state.driver)
    page.max_per_page()
    page.switch_to_tab(page.on_hold_tab)

    if filter is not None:
        field, value = filter.split(':', 1)
        page.filter_recordings(field, value)

    link_idx = 0
    while True:

        # kinda annoying that we have to do this each time
        page.refresh_off()

        try:
            # re-resolve the trim link elements each time because the refs go
            # stale when the page reloads
            # also, iterate via incrementing idx so that we don't somehow trim
            # the same thing > once (e.g. the entry doesn't get removed from
            # the table because the workflow hasn't actually resumed)
            link = page.trim_links[link_idx]
        except (TimeoutException,IndexError):
            break

        href = link.get_attribute('href')
        scheme, js = href.split(':', 1)
        page.js(js)
        page.switch_frame(page.trim_iframe)
        page = TrimPage(state.driver)
        page.trim()
        page.default_frame()
        page.reload()
        page = RecordingsPage(state.driver)

        if count is not None:
            count -= 1
            if count == 0:
                break

@cli.group()
@pass_state
def inbox(state):
    pass

@inbox.command(name='put')
@click.option('-f', '--file')
@inbox_options
@pass_state
@init_fabric
def inbox_put(state, file):
    result = put(local_path=file, remote_path=state.inbox_path, use_sudo=True)
    print(cyan("Files created: {}".format(str(result))))

@inbox.command(name='symlink')
@click.option('-f', '--file')
@click.option('-c', '--count', type=int, default=1)
@inbox_options
@pass_state
@init_fabric
def inbox_symlink(state, file, count):

    remote_path = state.inbox_dest.child(file)
    if not remote_exists(remote_path, verbose=True):
        abort("remote file {} not found".format(remote_path))

    with cd(state.inbox_path):
        for i in range(count):
            link = remote_path.stem + '_' + str(i + 1) + remote_path.ext
            sudo("ln -s {} {}".format(remote_path, link))
        return

@inbox.command(name='list')
@click.argument('match', default='')
@inbox_options
@pass_state
@init_fabric
def inbox_list(state, match):
    with cd(state.inbox_dest), hide('running', 'stdout', 'stderr'):
        output = run('ls {}'.format(match))
        for f in output.split():
            print(cyan(f))


if __name__ == '__main__':
    cli()
