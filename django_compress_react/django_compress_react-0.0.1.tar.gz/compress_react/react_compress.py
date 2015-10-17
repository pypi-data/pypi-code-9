from compressor.filters import FilterBase
from react.jsx import JSXTransformer
import os

# Logging support isn't readily available in compress
REACT_DEBUG = os.getenv("REACT_DEBUG", None)


class ReactFilter(FilterBase):

    def __init__(self, content, *args, **kwargs):
        if REACT_DEBUG:
            print("content :: {}".format(content))
            print("kwargs :: {}".format(kwargs))
        self.content = content
        kwargs.pop('filter_type')
        super(ReactFilter, self).__init__(content, *args, **kwargs)

    def input(self, **kwargs):
        if REACT_DEBUG:
            print("Process INPUT with :: {}".format(kwargs))
        try:
            t = JSXTransformer()
            rtn_str = t.transform_string(self.content)
        except Exception as e:
            """
                Given the way this can work for on the fly compression
                we'll print it out here and then raise the error; that way
                when using GUNICORN we can still see the error
            """
            print("Unable to process JSX :: {}".format(e))
            raise
        return rtn_str
