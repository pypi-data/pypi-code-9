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

from hatcher.core.utils import (
    NameVersionPairSorter,
    RuntimeMetadataV1,
)
from ..repository_actions import runtimes, _upload_verify
from ..utils import pass_repository, HTTPErrorHandlingUploadCommand


@runtimes.command('list', api_version=1)
@click.argument('organization')
@click.argument('repository')
@click.argument('platform')
@pass_repository
def list_runtimes_v1(repository, platform):
    """List all runtimes in a repository.
    """
    sort_key = lambda runtime: NameVersionPairSorter(*runtime)
    runtimes = sorted(
        repository.platform(platform).list_runtimes(),
        key=sort_key)
    headers = ['Runtime', 'Version']
    click.echo(tabulate(runtimes, headers=headers))


@runtimes.command('upload', help='Upload a single runtime to a repository.',
                  cls=HTTPErrorHandlingUploadCommand, api_version=1)
@click.argument('organization')
@click.argument('repository')
@click.argument('filename')
@click.option('--force', default=False, is_flag=True)
@click.option('--verify/--no-verify', default=False)
@pass_repository
def upload_runtime_v1(repository, filename, force, verify):
    def _do_upload():
        repository.upload_runtime(filename, overwrite=force)

    def _get_remote_metadata(local_metadata):
        repo = repository.platform(local_metadata.platform)
        return repo.runtime_metadata(
            local_metadata.implementation, local_metadata.version)

    _upload_verify(
        filename, _get_remote_metadata, RuntimeMetadataV1, _do_upload,
        verify=verify, force=force)


@runtimes.command('download', api_version=1)
@click.argument('organization')
@click.argument('repository')
@click.argument('platform')
@click.argument('implementation')
@click.argument('version')
@click.argument('destination', required=False)
@pass_repository
def download_runtime_v1(repository, platform, implementation, version,
                        destination=None):
    """Download a runtime archive.
    """

    if destination is None:
        destination = os.getcwd()

    length, iterator = repository.platform(platform).iter_download_runtime(
        implementation, version, destination)

    with click.progressbar(length=length) as bar:
        for chunk_size in iterator:
            bar.update(chunk_size)


@runtimes.command('metadata', help='Get the metadata for a single runtime.',
                  api_version=1)
@click.argument('organization')
@click.argument('repository')
@click.argument('platform')
@click.argument('implementation')
@click.argument('version')
@pass_repository
def runtime_metadata_v1(repository, platform, implementation, version):
    metadata = repository.platform(platform).runtime_metadata(
        implementation, version)
    click.echo(json.dumps(metadata, sort_keys=True, indent=2))
