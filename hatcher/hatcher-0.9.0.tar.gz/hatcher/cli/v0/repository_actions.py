#
# Canopy product code
#
# (C) Copyright 2013-2015 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is confidential and NOT open source.  Do not distribute.
#
import json
import os

import click
from tabulate import tabulate

from hatcher.core.utils import RuntimeV0Sorter, RuntimeMetadataV0
from ..repository_actions import runtimes, _upload_verify
from ..utils import pass_repository, HTTPErrorHandlingUploadCommand


@runtimes.command('list', api_version=0)
@click.argument('organization')
@click.argument('repository')
@click.argument('platform')
@pass_repository
def list_runtimes_v0(repository, platform):
    """List all runtimes in a repository.
    """
    sorted_filenames = sorted(repository.platform(platform).list_runtimes(),
                              key=RuntimeV0Sorter)
    runtimes = (RuntimeMetadataV0.from_file(name) for name in sorted_filenames)
    columns = [(runtime.language, runtime.full_version, runtime.python_tag)
               for runtime in runtimes]
    headers = ['Runtime', 'Version', 'Python Tag']
    click.echo(tabulate(columns, headers=headers))


@runtimes.command('upload', help='Upload a single runtime to a repository.',
                  cls=HTTPErrorHandlingUploadCommand, api_version=0)
@click.argument('organization')
@click.argument('repository')
@click.argument('filename')
@click.option('--force', default=False, is_flag=True)
@click.option('--verify/--no-verify', default=False)
@pass_repository
def upload_runtime_v0(repository, filename, force, verify):
    def _do_upload():
        repository.upload_runtime(filename, overwrite=force)

    def _get_remote_metadata(local_metadata):
        repo = repository.platform(local_metadata.platform)
        return repo.runtime_metadata(
            local_metadata.python_tag, local_metadata.full_version)

    _upload_verify(
        filename, _get_remote_metadata, RuntimeMetadataV0, _do_upload,
        verify=verify, force=force)


@runtimes.command('download', api_version=0)
@click.argument('organization')
@click.argument('repository')
@click.argument('platform')
@click.argument('python_tag')
@click.argument('version')
@click.argument('destination', required=False)
@pass_repository
def download_runtime_v0(repository, platform, python_tag, version,
                        destination=None):
    """Download a runtime archive.
    """

    if destination is None:
        destination = os.getcwd()

    length, iterator = repository.platform(platform).iter_download_runtime(
        python_tag, version, destination)

    with click.progressbar(length=length) as bar:
        for chunk_size in iterator:
            bar.update(chunk_size)


@runtimes.command('metadata', help='Get the metadata for a single runtime.',
                  api_version=0)
@click.argument('organization')
@click.argument('repository')
@click.argument('platform')
@click.argument('python_tag')
@click.argument('version')
@pass_repository
def runtime_metadata_v0(repository, platform, python_tag, version):
    metadata = repository.platform(platform).runtime_metadata(
        python_tag, version)
    print(json.dumps(metadata, sort_keys=True, indent=2))
