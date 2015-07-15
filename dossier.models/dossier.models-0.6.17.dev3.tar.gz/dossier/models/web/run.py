'''
Web services for active learning search engines
===============================================
This library ships with a command line application, ``dossier.models``,
that runs a web service. It is easy to run::

    dossier.models -c config.yaml

This runs it on ``localhost:8080``. A sample config file looks like:

.. code-block:: yaml

    dossier.store:
      feature_indexes: ['bowNP_sip', 'phone', 'region']

    dossier.models:
      tfidf_path: /path/to/tfidf/model.tfidf

    kvlayer:
      app_name: dossierstack
      namespace: myapp
      storage_type: redis
      storage_addresses: ['localhost:6379']

Where the ``tfidf_path`` corresponds to a TF-IDF model generated by
``gensim``. You can create one with the ``dossier.etl tfidf`` command.
(Note that this is optional!)

Once ``dossier.models`` is running, you can try the
Sorting Desk browser extension for Google Chrome:
https://chrome.google.com/webstore/detail/sorting-desk/ikcaehokdafneaiojndpmfbimilmlnid.
Once the extension is installed, you'll need to go to
its options and configure it to point to ``http://localhost:8080``.

Alternatively, you can follow the steps here to get a simple example
working on a sample data set:
https://github.com/dossier/dossier.models#running-a-simple-example.


Web service endpoints
---------------------
The web service has all of the same endpoints as :mod:`dossier.web`.
A couple of the endpoints are slightly enhanced to take advantage of
``dossier.models`` pairwise learning algorithm and feature extraction.
These enhanced endpoints are :func:`dossier.web.routes.v1_search` and
:func:`dossier.web.routes.v1_fc_put`. The ``v1_search`` endpoint is
enhanced with the addition of the :func:`dossier.models.similar` and
:func:`dossier.models.dissimilar` search engines. Additionally, the
``v1_fc_put`` accepts ``text/html`` content and will generate a feature
collection for you.


How the Sorting Desk browser extension works
--------------------------------------------
SortingDesk needs a ``dossier.models`` web server in order to function
properly. Namely, it uses ``dossier.models`` (and the underlying
DossierStack) to add/update feature collections, store ground truth
data as "labels," and run pairwise learning algorithms to rank relevant
search results. All of this information is saved to the underlying
database, so it is persistent across all user sessions.

``dossier.models`` also provides a folder/sub-folder organization
UI. Currently, this is built on top of Google Chrome's local storage.
Namely, it doesn't yet use the folder/subfolder web services described
in :mod:`dossier.web`. Therefore, folders/sub-folders don't yet persist
across multiple user sessions, but they will once we migrate off of
Chrome's local storage.
'''
from __future__ import absolute_import, division, print_function

import argparse
import logging

import bottle

import dblogger
from dossier.models.folder import Folders
from dossier.models.pairwise import dissimilar, similar
from dossier.models.web.config import Config
from dossier.models.web.routes import app as models_app
import dossier.web as web
import kvlayer
import yakonfig


logger = logging.getLogger(__name__)


class same_subfolder(web.Filter):
    def __init__(self, kvlclient, label_store):
        super(same_subfolder, self).__init__()
        self.kvl = kvlclient
        self.label_store = label_store
        self.folders = Folders(self.kvl)

    def create_predicate(self):
        subfolders = self.folders.parent_subfolders(self.query_content_id)
        cids = set()
        for folder_id, subfolder_id in subfolders:
            for cid, subid in self.folders.items(folder_id, subfolder_id):
                cids.add(cid)
                # Also add directly connected labels too.
                for lab in self.label_store.directly_connected((cid, subid)):
                    cids.add(lab.other(cid))
        return lambda (content_id, fc): content_id not in cids


def get_application():
    config = Config()
    p = argparse.ArgumentParser(description='Run DossierStack web services.')
    web.add_cli_arguments(p)
    args = yakonfig.parse_args(p, [dblogger, config, kvlayer, yakonfig])

    bottle.debug(True)
    app = (web.WebBuilder()
           .set_config(config)
           .enable_cors()
           .inject('tfidf', lambda: config.tfidf)
           .inject('google', lambda: config.google)
           .add_routes(models_app)
           .add_filter('already_labeled', same_subfolder)
           .add_search_engine('similar', similar)
           .add_search_engine('dissimilar', dissimilar)
           .get_app())
    return args, app


def main():
    args, app = get_application()
    app.run(server='wsgiref', host=args.host, port=args.port,
            debug=args.bottle_debug, reloader=args.reload)


if __name__ == '__main__':
    main()
