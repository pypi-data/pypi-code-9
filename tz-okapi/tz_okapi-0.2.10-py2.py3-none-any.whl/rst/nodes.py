from docutils.nodes import Special, FixedTextElement


class request_block(Special, FixedTextElement):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(request_block, self).__init__(*args, **kwargs)


class headers_block(Special, FixedTextElement):
    pass
