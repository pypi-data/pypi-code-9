#!/usr/bin/env python
import os
import time
import json

import click
import requests

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class EBAPostEventHandler(FileSystemEventHandler):

    def __init__(self, archive_path, config):
        self.archive_path = archive_path
        self.config = config

    def upload_file(self, src_file):
        config = self.config
        url = config["url"]

        click.echo("Uploading to: {}".format(url))
        r = requests.post(
            url,
            data={
                "key": config["key"],
                "user": config["user"],
                "delimiter": config["delimiter"],
                "bulk_format": config["bulk_format"],
                "upload_type": config["upload_type"],
                "organization": config["organization"],
            },
            files={"upload_file": open(src_file, "rb")}
        )
        click.echo("Uploaded {}".format(src_file))
        click.echo("{} {}".format(r.status_code, r.reason))

    def archive_file(self, src_file):
        os.rename(
            src_file,
            os.path.join(self.archive_path, os.path.basename(src_file))
        )
        click.echo("Archived {}".format(src_file))

    def dispatch(self, event):
        if event.is_directory:
            return
        return super(EBAPostEventHandler, self).dispatch(event)

    def on_created(self, event):
        self.upload_file(event.src_path)
        self.archive_file(event.src_path)


@click.command()
@click.option("--watch-path", type=click.Path(), required=True, help="path to watch")
@click.option("--archive-path", type=click.Path(), required=True, help="path to archive files to")
@click.option("--config", type=click.File(), required=True, help="JSON config file downloaded from EBAS")
@click.version_option()
def main(watch_path, archive_path, config):
    """
    watches a folder and auto-uploads files to an EBAS node with the given
    configuration for processing
    """
    config_data = json.load(config)

    event_handler = EBAPostEventHandler(archive_path, config_data)
    observer = Observer()
    observer.schedule(event_handler, watch_path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
