
import uuid
import json
import pandas as pd



class prettyjson(object):
    """
    Pretty display json or dictionnary in collapsible format with indents

    Options are
        depth: Depth of the json tree structure displayed, the rest is collapsed. By default: 2.
        max_length: Maximum number of characters of a string displayed as preview, longer string appear collapsed. By default: 20.
        sort: Whether the json keys are sorted alphabetically. By default: True.
        max_height: Maxium height in pixels of containing div. By default: 600.

    Examples:
        1/ Python dictionary
        dic = {'sape': {'value': 22}, 'jack': 4098, 'guido': 4127}
        prettyjson(dic, depth=1, max_length=10, sort=False)

        2/ json string
        json_str = '{"glossary": {"empty array": [], "empty object": {}, "string": "example glossary", "null field": null, "object": {"GlossList": {"GlossEntry": {"GlossDef": {"GlossSeeAlso": ["GML", "XML"], "para": "A meta-markup language, used to create markup languages such as DocBook."}, "GlossSee": "markup", "Acronym": "SGML", "GlossTerm": "Standard Generalized Markup Language", "Abbrev": "ISO 8879:1986", "SortAs": "SGML", "ID": "SGML"}}, "title": "S"}, "number": 2, "undefined field": "undefined", "boolean": false, "array": [3, 5]}}'
        prettyjson(json_str, depth=6, max_length=10, max_height=500)

    """

    def __init__(self, obj, **kwargs):

        def json_encode(obj):
            return pd.io.json.dumps(obj)

        def is_json(myjson):
            try:
                json_object = json.loads(myjson)
            except ValueError, e:
                return False
            return True

        if isinstance(obj, dict):
            self.json_str = json_encode(obj)
        elif is_json(obj):
            self.json_str = obj
        else:
            raise ValueError('Wrong Input, dict or json expected')
        
        self.uuid = str(uuid.uuid4())
        self.depth = kwargs.get('depth', 2)
        self.max_length = kwargs.get('max_length', 20)
        self.max_height = kwargs.get('max_height', 600)
        self.sort = json.dumps(kwargs.get('sort', True))
        self.renderjson = 'https://rawgit.com/caldwell/renderjson/master/renderjson.js'

        
    def _repr_html_(self):

        css = '<style>' + """
        .renderjson a              { text-decoration: none; }
        .renderjson .disclosure    { color: red;
                                     font-size: 125%; }
        .renderjson .syntax        { color: darkgrey; }
        .renderjson .string        { color: black; }
        .renderjson .number        { color: black; }
        .renderjson .boolean       { color: purple; }
        .renderjson .key           { color: royalblue; }
        .renderjson .keyword       { color: orange; }
        .renderjson .object.syntax { color: lightseagreen; }
        .renderjson .array.syntax  { color: lightseagreen; }
        """ + '</style>'
        
        html = """
            <div id="%s" style="max-height: %spx; width:100%%;"></div>
            """ % (self.uuid, self.max_height)
                
        js = """<script>
            require(["%s"], function() {
                document.getElementById("%s").appendChild(
                    renderjson.set_max_string_length(%s)
                              //.set_icons(circled plus, circled minus)                    
                              .set_icons(String.fromCharCode(8853), String.fromCharCode(8854))
                              .set_sort_objects(%s)
                              .set_show_to_level(%s)(%s))
            });</script>""" % (self.renderjson, self.uuid, self.max_length, self.sort, self.depth, self.json_str)
    
        return css+html+js





