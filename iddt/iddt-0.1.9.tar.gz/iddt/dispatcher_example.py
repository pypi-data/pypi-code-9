from iddt.dispatcher import Dispatcher

class MyDispatcher(Dispatcher):

    def __init__(self):
        super(MyDispatcher, self).__init__()

d = MyDispatcher()
d.dispatch({
    'target_url': 'http://timduffy.me/',
    'link_level': 3,
    'allowed_domains': [],
})

