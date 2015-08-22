import os
import glob
import pickle
import sys

import bottle


class RagoolView(bottle.Bottle, bottle.SimpleTemplate):
    """View application for ragool.
        It's already configured and ready to run.

        Sample usage :
            ragool = RagoolView()
            ragool.run()

    """
    def __init__(self, path=None):
        """Initialization of app.
            If you run it as standalone application
            then specify 'path' parameter.

            :param path:
                Directory where error files stored at

        """
        bottle.Bottle.__init__(self)
        bottle.TEMPLATE_PATH.insert(0, os.path.dirname(__file__))
        if not path:
            self.r_path = os.path.dirname(
                os.path.realpath(sys.argv[0]))+"/ragool"
        else:
            self.r_path = path

        self.route('/', callback=self.index_view)
        self.route('/<error>', callback=self.error_view, name='error')

        self.defaults['request'] = bottle.request
        self.defaults['url_for'] = self.get_url

    def index_view(self):
        data = []
        for file in glob.glob(self.r_path+'/*'):
            data.append((file, pickle.load(open(file, 'rb'))))
        return bottle.template('ragool-template.html', data=data)

    def error_view(self, error):
        data = pickle.load(open(self.r_path+'/'+error, 'rb'))
        return bottle.template('ragool-template.html', data=data)