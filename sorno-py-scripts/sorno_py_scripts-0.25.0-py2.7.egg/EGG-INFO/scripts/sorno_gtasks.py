#!/usr/bin/python
"""A command line client for Google Tasks

It's done by following the tutorials in Google Developers:
https://developers.google.com/google-apps/tasks/quickstart/python.

In order to use this script, please look at the "Using scripts involve Google
App API" section of the sorno-py-scripts README (can be found in
https://github.com/hermantai/sorno-scripts/tree/master/sorno-py-scripts). The
API needed for this script is "Tasks API" with the scope
'https://www.googleapis.com/auth/tasks'.

Examples:

    To print tasks for all of your task lists:

        $ sorno_gtasks.py get_tasks

    To print task only for your task list "list1" and "list2":

        $ sorno_gtasks.py get_tasks list1 list2


    Copyright 2014 Herman Tai

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import argparse
import httplib2
import logging
import os
import pprint
import subprocess
import sys

from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client import tools

from sorno import loggingutil


# The oauth scope needed for Google Tasks API
OAUTH_SCOPE = 'https://www.googleapis.com/auth/tasks'

# The file path that stores the access token returned by Google from oauth
# authentication
CREDENTIALS_FILE = os.path.expanduser("~/.sorno_gtasks-google-drive-api.cred")

_log = logging.getLogger(__name__)
_plain_logger = None  # will be created in main()
_plain_error_logger = None  # will be created in main()


class GoogleTasksConsoleApp(object):
    """The controller of the sorno_gtasks script"""

    def __init__(
        self,
    ):
        self.tasks_service = None

    def auth(self, flags, use_credentials_cache=True):
        """
        Authenticates either by an existing credentials or by prompting the
        user to grant permissions. If succeeds, set self.tasks_service to the
        service client that can call tasks api. Otherwise, it aborts the
        script.

        Args:
            flags (argparse.Namespace): The flags for this script
            use_credentials_cache (Optional[bool]): If true, uses the
                credentials stored in ``CREDENTIALS_FILE``.
        """
        # Copy your credentials from the console
        client_id = os.getenv('GOOGLE_APP_PROJECT_CLIENT_ID')
        client_secret = os.getenv('GOOGLE_APP_PROJECT_CLIENT_SECRET')

        if not client_id:
            _log.info(
                "Please set the environment variable"
                " GOOGLE_APP_PROJECT_CLIENT_ID"
            )
            sys.exit(1)

        if not client_secret:
            _log.info(
                "Please set the environment variable"
                " GOOGLE_APP_PROJECT_CLIENT_SECRET"
            )
            sys.exit(1)

        # Run through the OAuth flow and retrieve credentials
        flow = OAuth2WebServerFlow(
            client_id,
            client_secret,
            OAUTH_SCOPE,
        )

        # Indicate we need the user to grant us permissions and give the auth
        # code or not
        need_get_code = True

        storage = Storage(CREDENTIALS_FILE)
        if os.path.exists(CREDENTIALS_FILE) and use_credentials_cache:
            credentials = storage.get()
            _log.debug("Use old credentials")
            need_get_code = False

        if need_get_code:
            credentials = tools.run_flow(flow, storage, flags)

        # Create an httplib2.Http object and authorize it with our credentials
        http = httplib2.Http()
        http = credentials.authorize(http)

        self.tasks_service = build('tasks', 'v1', http=http)

    def get_tasks_action(self, args):
        """Handle the subcommand get_tasks

        Print out the tasks for the task lists specified from the flags of the
        script.

        Args:
            args (argparse.Namespace): The flags of the script.
        """
        self.auth(args, use_credentials_cache=args.use_credentials_cache)

        tasklists_names = args.tasklist or []
        tasklists = self.get_tasklists()
        tasklists_to_show = []

        tasklists_map = {
            tasklist['title']: tasklist for tasklist in tasklists
        }

        if not tasklists_names:
            # assume all the task lists if no task lists are provided
            tasklists_to_show.extend(tasklists)
        else:
            for tasklist_name in tasklists_names:
                if tasklist_name not in tasklists_map:
                    _plain_error_logger.error(
                        "Task list [%s] does not exist. Avaliable task lists"
                            " are:",
                        tasklist_name,
                    )
                    for index, tasklist in enumerate(tasklists, 1):
                        if args.detail:
                            s = pprint.pformat(tasklist)
                        else:
                            s = tasklist['title']
                        _plain_logger.error("%d) %s", index, s)
                    return 1
                tasklists_to_show.append(tasklists_map[tasklist_name])

        for tasklist_to_show in tasklists_to_show:
            tasklist_id = tasklist_to_show['id']

            if args.detail:
                s = pprint.pformat(tasklist_to_show)
            else:
                s = "[%s]:" % tasklist_to_show['title']

            _plain_logger.info(
                "Tasks for the list %s",
                s,
            )
            tasks = self.get_tasks_from_tasklist(tasklist_id)
            for index, task in enumerate(tasks, 1):
                if args.detail:
                    s = pprint.pformat(task)
                else:
                    s = task['title']
                _plain_logger.info("%d) %s", index, s)
                if args.with_notes:
                    _plain_logger.info("Notes: %s", task.get('notes', ""))

        return 0


    def get_tasklists(self):
        """Retrieve the task lists of the user

        Returns:
            A list of dictionaries each represents a Tasklist resource.

            {
              "kind": "tasks#taskList",
              "id": string,
              "etag": string,
              "title": string,
              "updated": datetime,
              "selfLink": string
            }
        """

        results = self.tasks_service.tasklists().list().execute()
        return results.get('items', [])

    def get_tasks_from_tasklist(self, tasklist_id):
        """Retrieves a list of tasks for a Tasklist

        Args:
            tasklist_id (string): The ID of the Tasklist.

        Returns:
            A list of dictionaries each represents a Task resource.

            {
              "kind": "tasks#task",
              "id": string,
              "etag": etag,
              "title": string,
              "updated": datetime,
              "selfLink": string,
              "parent": string,
              "position": string,
              "notes": string,
              "status": string,
              "due": datetime,
              "completed": datetime,
              "deleted": boolean,
              "hidden": boolean,
              "links": [
                {
                  "type": string,
                  "description": string,
                  "link": string
                }
              ]
            }
        """
        results = self.tasks_service.tasks().list(
            tasklist=tasklist_id
        ).execute()
        return results.get('items', [])


def parse_args(app_obj, cmd_args):
    description = __doc__.split("Copyright 2014")[0].strip()

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[tools.argparser],
    )
    parser.add_argument(
        "--no-credentials-cache",
        dest="use_credentials_cache",
        action="store_false",
        default=True,
        help="If specified, old credentials are not reused and you have to"
            " follow the instruction from this script to get the code every"
            " time you use this script.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
    )

    subparsers = parser.add_subparsers(
        title="Subcommands",
        description="Some description for subcommands",
    )

    get_tasks_description = """Print tasks for your task lists.

Examples:

    To print tasks for all of your task lists:

        $ sorno_gtasks.py get_tasks

    To print task only for your task list "list1" and "list2":

        $ sorno_gtasks.py get_tasks list1 list2

By default, get_tasks only prints the titles of your tasks. You can use
--with-notes option to print the notes as well. Use the --detail option to
show details.

Examples:

    To show the details for all tasks and all task lists.

        $ sorno_gtasks.py get_tasks --detail
    """

    parser_get_tasks = subparsers.add_parser(
        "get_tasks",
        help="Print your tasks",
        description=get_tasks_description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser_get_tasks.add_argument(
        "--with-notes",
        action="store_true",
        help="shows the notes for each task",
    )
    parser_get_tasks.add_argument(
        "--detail",
        action="store_true",
        help="see the details for all tasks and task lists",
    )
    parser_get_tasks.add_argument(
        "tasklist",
        nargs="*",
        help="The tasks in which to be printed out. If not specified, "
        " assume all tasks in all task lists.",
    )
    parser_get_tasks.set_defaults(func=app_obj.get_tasks_action)

    args = parser.parse_args(cmd_args)
    return args


def main():
    global _plain_logger, _plain_error_logger

    app = GoogleTasksConsoleApp()
    args = parse_args(app, sys.argv[1:])

    loggingutil.setup_logger(_log, debug=args.debug)
    _plain_logger = loggingutil.create_plain_logger(
        "PLAIN",
        debug=args.debug,
    )
    _plain_error_logger = loggingutil.create_plain_logger(
        "PLAIN_ERROR",
        debug=args.debug,
        stdout=False,
    )
    args.func(args)


if __name__ == '__main__':
    main()
