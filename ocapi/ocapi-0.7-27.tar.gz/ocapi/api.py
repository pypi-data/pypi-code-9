#!/usr/bin/env python
# -*- coding:utf-8 -*-
# (c)Ing. Zdenek Dlauhy, Michal Dlauhy, info@dlauhy.cz


"""
ocapi
=====

This is API connector to www.pripravto.cz service for furniture makers. You should
be able to use it to create your custom designs for furniture, download data
and eventually build your partial interface. Connector is built on HTTP GET and
POST methods and it uses your account on service.

This connector can also be used to build custom api connection to another services.

Instalation
-----------

For instalation you can download package or install by **pip**. Downloaded you
can just unpack or get from from https://pypi.python.org/pypi/ocapi and install it::

    #download archive
    wget https://bitbucket.org/pripravto/ocapi/get/default.tar.gz
    cd /tmp
    virtualenv test
    source test/bin/activate
    tar -xvf default.tar.gz
    #specify correct name
    cd pripravto....

Instalation::

    python setup.py install

or install by pip::

    pip install ocapi


Quickstart
----------

First you should get your account on **https://pripravto.cz** service, when you will have it
Login normally into service. Then you can start by opening Python console
and importing ocapi::

    import ocapi.api as oc
    import math
    args = {'name':'test2','position':[0,0,0],'size':[1000,1000,1000]}
    #set your own credentials will log error with these use credentials
    prod = oc.CabinetMaker(args, username="test",password="test")
    for i in range(36):
        size = [18,math.sin(math.radians(i*10))*50+80,18]
        rot = [0,0,10+i*2]
        prod.add_element(pos=[i*20,0,0],size=size,rot=rot)
    prod.finish()

This is partial example which will show you base usage of this api. This will create
serries of elements which are sized by sin function and rotated by series of
iteration.

To build something more usefull you can make first base cabinet by just writing down
one function::

    args = {'name':'cabinet2','position':[0,0,0],'size':[600,600,1000]}
    prod.parse_args(args)
    #build our base parts
    prod.add_basic()
    #add doors
    prod.add_doors()
    prod.finish()

After data creation you can also check what kind of data you have created on service
itself and also download images and so on.

Username and password are specified at start of object::

    prod = oc.CabinetMaker(args, username="test",password="test", host="test.pripravto.cz")
    #your username and password is from https://pripravto.cz/register/start

For complete registration process you need your functional e-mail address and fill out
data required by registration. **You should keep your user credentials secret.**
For examples what can be built on this api connector take a look on http://pripravto.cz/en/blog
where we put examples.

More documantation for pripravto service or about this plase see web page or
**oc.CabinetMaker** class.

Development
-----------

You can contact us or raise issues on https://bitbucket.org/pripravto/ocapi
Developmnet is also made on Bitbucket, you can clone repository and start
making chaneges. We also plan to use this api connector to be able to connect
with diffrent applications more quickly and easily.

For this project we are using PyVmMonitor on http://www.pyvmmonitor.com


module for access to oc api

base usecase::

    import ocapi.api as oc
    import math
    args = {'name':'test2','position':[0,0,0],'size':[1000,1000,1000]}
    prod = oc.CabinetMaker(args, username="test",password="test")

    for i in range(36):#count through whole rotation
        size = [18,math.sin(math.radians(i*10))*50+80,18]#change size
        rot = [0,0,10+i*2]#rotate part
        prod.add_element(pos=[i*20,0,0],size=size,rot=rot)
    prod.finish()

"""

import uuid
import json
import ocapi.info as info

import sys

if sys.platform == "brython":
    # first hook up brython version
    # do not make imports if they are not needed
    # it is slow.....
    # get connection object for ajax browser
    import ocapi.brythonapi
    str.encode = lambda x, y: x
    str.decode = lambda x, y: x
    convert_to_base = lambda x:x
    basestring = str
    connect = ocapi.brythonapi.Connection
    log = ocapi.brythonapi.log
    base64_decode = ocapi.brythonapi.window.atob

else:
    # here is normal python
    import ocapi.urllibtls
    connect = ocapi.urllibtls.connect
    import logging
    import functools
    import os
    import base64
    logging.basicConfig(level=0)
    log = logging.getLogger(__name__)
    import collections
    base64_decode = base64.decodestring
    def convert_to_base(data):
        """
        convert data input to base types
        """
        if isinstance(data, basestring):
            try:
                return str(data.encode('utf-8'))
            except UnicodeDecodeError:
                return str(data)
        elif isinstance(data, collections.Mapping):
            return dict(map(convert_to_base, data.items()))
        elif isinstance(data, collections.Iterable):
            return type(data)(map(convert_to_base, data))
        else:
            return data


class AttrDict(dict):
    def __getattr__(self, attr):
        return self[attr]
    def __setattr__(self, attr, value):
        self[attr] = value

def api_generator(save=True):
    """
    function for api generation which creates code
    for base CabinetMaker class. This function can be used only in full OptimCabinet
    framework. It will not work without several other functions.
    """
    klass = """
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# (c)Ing. Zdenek Dlauhy, Michal Dlauhý, info@dlauhy.cz

class CabinetMakerBase(object):
"""
    funcs_def = """
    def {func}(self, {parameters}):
        '''{doc}'''
        _loc = dict(locals())
        _loc.pop('self')
        self.custom_action(method='{func}', **_loc)

"""
    def attach_attrs(attrs):
        """attach parameters inside template"""
        return ",".join("{}={}".format(k, "'{}'".format(v) if isinstance(v, str) else v) for k, v in sorted(attrs.items()))
    # this import needs whole optimcabinet
    import initialization as oc
    import webapp.web_products
    # get base data
    doc = webapp.web_products.product_doc_generator(oc.CabinetMaker)
    funcs = webapp.web_products.product_parameters_generator(oc.CabinetMaker, generate=True, make_all=True)
    all_data = {}
    # merge data together
    for key, value in funcs:
        all_data[key] = {'attrs':value}
    for key, value in doc:
        all_data[key]['doc'] = value
    all_funcs_def = {}
    # make function definition
    for key, value in all_data.items():
        all_funcs_def[key] = funcs_def.format(func=key,
                                              parameters=attach_attrs(value['attrs']),
                                              doc=value['doc'])
    # merge whole document and save it
    klass += "".join(v for k, v in all_funcs_def.items())
    if save:
        filename = os.path.abspath(__file__)
        path, filename = os.path.split(filename)
        writer = open("{}/product.py".format(path), "w")
        writer.write(klass)
        writer.close()
    return klass

# import local api of CabinetMaker
try:
    from ocapi.product import CabinetMakerBase
except ImportError as e:
    log.error(e)
    log.error("Run api generator")


class BaseControl(object):
    """
    base object for web api access
    initialize connection to some webservice
    """
    def __init__(self, username='user', password='pass', host="example.com",
                 port=443, debug=None, connector=connect, filepath="/tmp",
                 tls=True, raise_error=False):
        """
        :param username: username of user accessing service
        :type username: str
        :param password: password of user accessing service
        :type password: str
        :param host: base name of domain
        :type host: str
        :param port: port to connect
        :type port: int
        :param debug: set debug level
        :type debug: int or None
        :param connector: set connector function
        :type connector: func
        """
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.debug = debug
        self.cookie = None
        self.connector = connector
        self.filepath = filepath
        self.tls = tls
        self.raise_error = raise_error
        log.info("Creating connection {}".format(self))

    def __del__(self):
        log.info("Finishing all connections on {}".format(self))

    def login(self, username=None, password=None, url="/login"):
        """base login action"""
        if username is None:
            username = self.username
        if password is None:
            password = self.password
        data = dict(username=username, passwd=password)
        response = self.action(url=url, data=data, method="POST")
        if response.status == 302:
            # get cookie or start app
            headers = self.get_headers(response)
            cookie = headers.get("set-cookie", None)
            if cookie:
                self.cookie = cookie.split(";")[0]
            location = headers.get("location", None)
            if location == "/oc/start":
                import time
                # start app
                response = self.action(url=location)
                log.info("Waiting for app to start!")
                time.sleep(5)
        return response

    def action(self, url, data=None, host=None, method="GET", headers=None,
               convert=None, tls=None, port=None):
        """function which makes action ie. download file and send data"""
        if host is None:
            host = self.host
        if port is None:
            port = self.port
        if tls is None:
            tls = self.tls
        log.debug("Contacting url {}:{}{} with {}".format(host, port, url, data))
        response = self.connector(host=host, url=url, port=port, data=data, method=method,
                                  headers=headers, debug=self.debug, cookie=self.cookie,
                                  tls=tls)
        if response.status < 400:
            if convert:
                return convert(response)
            else:
                return response
        else:
            msg = "Error in connecting requested url {}:{}"
            log.error(msg.format(response.reason, response.status))
            return self.check_response(response)

    def save_file(self, response, headers=None):
        """save file if response should be file"""
        if headers is None:
            headers = self.get_headers(response)
        if headers.get("content-disposition", False):
            filename = headers["content-disposition"].split("filename=")[-1]
        else:
            filename = str(uuid.uuid4())
        if headers.get("content-transfer-encoding", None) == "base64":
            data = base64_decode(response.read())
        else:
            data = response.read()
        filename = "{}/{}".format(self.filepath, filename)
        if sys.platform != "brython":
            with open(filename, 'wb') as writer:
                writer.write(data)
                writer.close()
                log.info("File saved to {}".format(filename))
            return filename
        return data

    def get_headers(self, response):
        """make headers same on Python2 and 3"""
        headers = dict(response.getheaders())
        headers = {key.lower():value for key, value in headers.items()}
        return headers

    def check_response(self, response):
        if response.status >= 400 and self.raise_error:
            raise Exception("Server response {}".format(response.status))
        else:
            return response

    def convert(self, response, headers=None):
        """automated convertor function which when is used in self.action
        changes what will happen with response
        """
        if response.status == 200:
            if headers is None:
                headers = self.get_headers(response)
            headers['content-type'] = headers.get('content-type', None)
            log.info("Converting data sources {} {}".format(response, headers['content-type']))
            if headers['content-type'] == 'text/xml' or headers['content-type'] == 'application/xml':
                try:
                    import inout.optimio
                    return inout.optimio.xml2obj(response.read())
                except ImportError as e:
                    log.error(e)
                    return response
            elif headers['content-type'] == 'text/json' or headers['content-type'] == 'application/json':
                return convert_to_base(json.loads(response.read().decode("utf-8")))
            elif headers['content-type'] == 'image/svg+xml' or headers['content-type'] == 'image/jpeg':
                return self.save_file(response, headers)
            elif headers['content-type'] == 'text/plain':
                text = response.read().decode("utf-8")
                log.warn(text)
                return text
            elif headers.get("content-disposition", False):
                return self.save_file(response, headers)
        return response

class Control(BaseControl):
    """
    this class creates alll basic method which will be needed
    to control web app. It does not create production functions
    and also it should just set and receive data
    """

    def other_funcs(self):
        """attach other functions"""
        self.action_list = {'commit':'/rev/commit',
                            'new':'/system/new',
                            'save':'/system/savepickle'}
        self.make_funcs(self.action_list)

    def make_funcs(self, actions):
        """make functions based on actions list with partial"""
        import functools
        for key, value in actions.items():
            func = functools.partial(self.action, url=value, convert=self.convert)
            setattr(self, key, func)

    def get_optim(self, name=None, obj_id=None, make_new=False):
        """get optim details"""
        return self.get_optim_calc(template="optimalize", name=name,
                                   obj_id=obj_id, make_new=make_new)

    def get_optim_calc(self, template="optimalize", name=None, obj_id=None, make_new=True):
        """
        :param template: template to get
        :type template: str
        :param name: get requested order
        :type name: str
        :param obj_id: get requested id
        :type obj_id: int
        :param make_new: create new calculation or optimalization
        :type make_new: bool
        """
        log.info("Trying to download data for {}".format(template))
        if name is None:
            name = self.get_order_name()
        if make_new:
            response = self.action(url="/{}/".format(template))
        if obj_id is None:
            last_calc = self.action(url="/json/{}/orders".format(template), convert=self.convert)
            # count from 0
            obj_id = last_calc[name] - 1
        url = "/json/{}/orders/{}/{}".format(template, name, obj_id)
        return self.action(url=url, convert=self.convert)

    def get_calc(self, name=None, obj_id=None, make_new=False):
        """get calculation details"""
        return self.get_optim_calc(template="calculation", name=name,
                                   obj_id=obj_id, make_new=make_new)

    def get_prod_name(self, name=None):
        if name is None:
            name = getattr(self, "name", "untitled")
        return name

    def get_order_name(self):
        """get name of opened order"""
        response = self.action(url="/json/sidebar", convert=self.convert)
        return str(response['order'])

    def get_product(self, name=None):
        """get actual product data"""
        name = self.get_prod_name(name)
        return self.action(url="/json/products/{}".format(name), convert=self.convert)

    def get_product_all(self, name=None):
        """get actual product data"""
        name = self.get_prod_name(name)
        res = self.action(url="/json/products/{}/all".format(name), convert=self.convert)
        prod = AttrDict(res)
        return prod

    def get_products_all(self):
        """get all products at once"""
        res = self.action(url="/json/products_all", convert=self.convert)
        prod = AttrDict(res)
        return prod

    def get_element(self, element, product=None):
        """get element object from json"""
        product = self.get_prod_name(product)
        element = self.action(url="/json/products/{}/{}".format(product, element), convert=self.convert)
        return AttrDict(element)

    def get_element_from_product(self, product, element):
        if isinstance(element, int):
            element = product['data'][str(element)]
        return AttrDict(product['elements'][element])

    def get_order(self, name=None):
        """get actual order data"""
        if name is None:
            name = self.get_order_name()
        return self.action(url="/json/orders/{}".format(name), convert=self.convert)

    def get_image(self, name=None, order=None, paths=None, typ="product", url=None,
                  convert=True):
        """
        :param name: specify product name
        :type name:
        :param order: specify order name
        :type order:
        :param paths: send paths to select
        :type paths:
        :param typ: choose type
        :type typ:
        :param url: url to get image
        :type url: 
        :param convert: save file or no
        :type convert:
        
        get image based on settings"""
        log.info("Trying to download image")
        if paths is None:
            paths = {'element':'products/elements',
                     'product':'products',
                     'product_viz':'products/viz',
                     'optim':'optim',
                     'viz':'products/viz',
                     'img':'import'}
        name = self.get_prod_name(name)
        if order is None:
            order = self.get_order_name()
        if typ == "product":
            name = "{}_{}.svg".format(order, name)
        elif typ == "optim":
            pass
        elif typ == "product_viz":
            name = "{}_{}.jpeg".format(order, name)
        elif typ == "viz":
            name = "{}.jpeg".format(order)
        else:
            raise Exception("Wrong type of requested image")
        if url is None:
            url = "/userdata/{}/{}".format(paths[typ], name)
        if convert:
            image = self.action(url=url, convert=self.convert)
        else:
            image = self.action(url=url)
        return image

    def load_products(self, name):
        """load order by saved name of pickle"""
        return self.action(url="/system/loadpickle{}".format(name))

    def save_products(self):
        response = self.action(url="/system/savepickle")
        response = self.action(url="/rev/commit")

    def custom_action(self, method="name", **kwargs):
        """custom action to save data"""
        self.data.append((method, kwargs))

    def add_empty(self, func_key='add_empty', **kwargs):
        '''
        special function here we assume that function is empty
        and should be handled by server so we remove not needed data and
        also func_key which would collide with server version
        '''
        loc = dict(locals())
        loc.pop('self')
        loc.update(loc['kwargs'])
        loc.pop('kwargs')
        loc.pop('func_key')
        self.custom_action(method=func_key, **loc)


class CabinetMaker(Control, CabinetMakerBase):
    """
    This Class gets product functions from cabinet maker class which
    can be dynamically generated by api_generator function.

    This Class is created to construct products as original cabinet maker

    example::

        import ocapi.api as oc
        import math
        args = {'name':'test2','position':[0,0,0],'size':[1000,1000,1000]}
        prod = oc.CabinetMaker(args, username="test",password="test")
        for i in range(36):#count through whole rotation
            size = [18,math.sin(math.radians(i*10))*50+80,18]#change size
            rot = [0,0,10+i*2]#rotate part
            prod.add_element(pos=[i*20,0,0],size=size,rot=rot)
        prod.finish()

    """
    def __init__(self, args=None, username='user', password='pass', host="test.pripravto.cz",
                 port=443, debug=None, connector=connect, filepath="/tmp",
                 login=True, tls=True, raise_error=False):
        BaseControl.__init__(self, username=username, password=password, host=host, port=port,
                             debug=debug, connector=connector, filepath=filepath, tls=tls,
                             raise_error=raise_error)
        self.data = []
        self.name = "untitled"
        if args:
            self.parse_args(args)
        if login and sys.platform != "brython":
            self.login(username, password)

    def parse_args(self, params):
        """transform parameters into type used on web service"""
        params = dict(params)
        params['posX'] = params['position'][0]
        params['posY'] = params['position'][1]
        params['posZ'] = params['position'][2]
        params['width'] = params['size'][0]
        params['depth'] = params['size'][1]
        params['height'] = params['size'][2]
        params['selectFunction'] = "empty"
        self.name = params.get('name', "untitled")
        params.pop('position')
        params.pop('size')
        self.data = self.data + list(params.items())
        self.data.append(('productParam', params))

    def recreate_product_data(self, product):
        """create again data source for new send to service"""
        self.data = []
        self.parse_args(product.arg)
        self.data += [(list(obj.keys())[0], list(obj.values())[0]) for obj in product.data_functions]
        log.info("Prepared data for next product creation.")

    def finish(self, get_error=True):
        """send all data to server and create object"""
        log.info("To create new product use func parse_args")
        name = self.name
        response = self.action(url="/products/create", data=self.data, method='POST')
        if get_error:
            error = self.action(url="/json/lasterror", convert=self.convert)
        else:
            error = None
        if error:
            msg = "Error in {} with parameter {}"
            raise Exception(msg.format([error['func_name']], [error['actual_error']]))
        else:
            log.info("Product created. Removing old data and returning new product")
            self.data = []
            response = self.get_product_all(name)
            return response

    def make_funcs(self, actions, docs):
        """create all functions so it should be possible to use it as cabinet maker"""
        for key, value in actions:
            func = functools.partial(self.custom_action, method=key, **value)
            setattr(self, key, func)
        for key, value in docs:
            func = getattr(self, key)
            func.__doc__ = value




if __name__ == "__main__" :
    # api_generator()
    # import ocapi.api as oc
    import math
    
    def test_local():
        args = {'name':'test2', 'position':[0, 0, 0], 'size':[1000, 1000, 1000]}
        prod = CabinetMaker(args, host="localhost", port=2000, tls=False, login=False)
        for i in range(36):  # count through whole rotation
            size = [18, math.sin(math.radians(i * 10)) * 50 + 80, 18]  # change size
            rot = [0, 0, 10 + i * 2]  # rotate part
            prod.add_element(pos=[i * 20, 0, 0], size=size, rot=rot)
        print(prod.finish())
        print(prod.get_image())


    def test_local_get_calc():
        prod = CabinetMaker(None, host="localhost", port=2000, tls=False, login=False)
        prod.action("/system/new")
        prod.action("/orders/create?name=dva&info=Data&customer=Alfonz")
        args = {'name':'test2', 'position':[0, 0, 0], 'size':[1000, 1000, 1000]}
        prod.parse_args(args)
        for i in range(36):  # count through whole rotation
            size = [18, math.sin(math.radians(i * 10)) * 50 + 80, 18]  # change size
            rot = [0, 0, 10 + i * 2]  # rotate part
            prod.add_element(pos=[i * 20, 0, 0], size=size, rot=rot)
        data = list(prod.data)
        print(prod.finish())
        print(prod.get_calc(make_new=True))
        print(prod.get_image())

    def test_get_products():
        con = CabinetMaker(None, host="localhost", port=2000, tls=False, login=False)
        con.name = "dunt_51"
        prod = con.get_product_all()
        size = prod.size
        element = AttrDict(prod.elements['dunt_51_0_BOK'])
        calc = element.calculation
        con.recreate_product_data(prod)
        con.custom_action(method="add_shape_cut", origin=None, tool_side='center', pos=None, number=4, joint='add_shape_cut_round', shape=True, radius=100, x_dist=100, tool_side_close='center', rot=None, size=None, tool_diameter=10, index=None, y_dist=100, process_type='acamProcessROUGH_FINISH', tool_number=1, final_depth=0, planes=None, save=True)
        prod = con.finish()
        con.recreate_product_data(prod)
        element = AttrDict(prod.elements['dunt_51_6_POL'])
        dat = [{'type':'line', 'pos':[0, 20, 0], 'pos1':[element.sizeLength - 20, 20, 0]}, {'type':'line', 'pos':[element.sizeLength - 20, 20, 0], 'pos1':[element.sizeLength - 20, element.sizeWidth - 20, 0]}]
        con.custom_action(method="add_shape_cut", joint=dat, index='dunt_51_6_POL', shape=False, save=True)
        prod = con.finish()


    def test_change_product():
        args = {'edgeSIDE': ['Z', 0, 0, 0], 'thickConstr': 18, 'frontOut': False, 'socle': 0, 'matSteel': 'F509', 'matBack': '101', 'size': [600, 510, 900], 'style': 'FLAT', 'thickDrawer': 18, 'thickBack': 5, 'edgeDRAWER': ['X', 0, 0, 0], 'frame_width': 70, 'edgeTOP': ['Z', 0, 0, 0], 'matConstr': 'H3702', 'edges': True, 'elementInfo': {'fittings': {'KOL': 5}, 'production': {'EDGEBANDER': 2, 'HAND': 3, 'SAW': 1, 'COATING': False, 'CNC': 1}, 'group': 'dunt_17', 'visibility': 'NORMAL', 'block': True}, 'rotation': [0, 0, 0], 'matFront': 'H3702', 'product_type': 'product', 'name': 'dunt_17', 'position': [0, 0, 0], 'edgeDOOR': ['Z', 'Z', 'Z', 'Z']}
        con = CabinetMaker(args, host="localhost", port=2000, tls=False, login=False)
        con.add_basic(info=None, top_bars=None, variant='H', area_id=None, socle=None, back=5, diff=None, save=True)
        con.add_shelve(info=None, area_id=None, mat=None, number=None, diff=None, rotation=None, save=True, size=None)
        con.finish()
        prod = con.get_product_all()
        print(prod)
        con.recreate_product_data(prod)
        for i in [0, 1, 2, 3, 4]:
            el_name = prod.data[str(i)]
            element = AttrDict(prod.elements[el_name])
            thick = element.sizeThickness
            con.add_mod_element(index=i, sizeThickness=thick + 20)
        prod = con.finish()


    def test_change_product_2():
        args = {'edgeSIDE': ['Z', 0, 0, 0], 'thickConstr': 18, 'frontOut': False, 'socle': 0, 'matSteel': 'F509', 'matBack': '101', 'size': [600, 510, 900], 'style': 'FLAT', 'thickDrawer': 18, 'thickBack': 5, 'edgeDRAWER': ['X', 0, 0, 0], 'frame_width': 70, 'edgeTOP': ['Z', 0, 0, 0], 'matConstr': 'H3702', 'edges': True, 'elementInfo': {'fittings': {'KOL': 5}, 'production': {'EDGEBANDER': 2, 'HAND': 3, 'SAW': 1, 'COATING': False, 'CNC': 1}, 'group': 'dunt_17', 'visibility': 'NORMAL', 'block': True}, 'rotation': [0, 0, 0], 'matFront': 'H3702', 'product_type': 'product', 'name': 'dunt_17', 'position': [0, 0, 0], 'edgeDOOR': ['Z', 'Z', 'Z', 'Z']}
        con = CabinetMaker(args, host="localhost", port=2000, tls=False, login=False)
        for i in range(0, 40):
            con.add_element(number=1, pos=[0, 0, 0])
        con.finish()
        prod = con.get_product_all()
        print(prod)
        con.recreate_product_data(prod)
        for i in range(0, 40):
            el_name = prod.data[str(i)]
            element = AttrDict(prod.elements[el_name])
            thick = element.sizeThickness
            con.add_mod_element(index=i, elementRotation=[10 * i, 0, 0])
        prod = con.finish()

    def test_normal():
        args = {'name':'test2', 'position':[0, 0, 0], 'size':[1000, 1000, 1000]}
        prod = CabinetMaker(args, username="useroc1", password="oc1user1piff")
        for i in range(36):  # count through whole rotation
            size = [18, math.sin(math.radians(i * 10)) * 50 + 80, 18]  # change size
            rot = [0, 0, 10 + i * 2]  # rotate part
            prod.add_element(pos=[i * 20, 0, 0], size=size, rot=rot)
        print(prod.finish())
        print(prod.get_image())


    def test_bigger():
        args = {'edgeSIDE': ['Z', 0, 0, 0], 'thickConstr': 18, 'frontOut': False, 'socle': 0, 'matSteel': 'F509', 'matBack': '101', 'size': [600, 510, 900], 'style': 'FLAT', 'thickDrawer': 18, 'thickBack': 5, 'edgeDRAWER': ['X', 0, 0, 0], 'frame_width': 70, 'edgeTOP': ['Z', 0, 0, 0], 'matConstr': 'H3702', 'edges': True, 'elementInfo': {'fittings': {'KOL': 5}, 'production': {'EDGEBANDER': 2, 'HAND': 3, 'SAW': 1, 'COATING': False, 'CNC': 1}, 'group': 'dunt_71', 'visibility': 'NORMAL', 'block': True}, 'rotation': [0, 0, 0], 'matFront': 'H3702', 'product_type': 'product', 'name': 'dunt_71', 'position': [0, 0, 0], 'edgeDOOR': ['Z', 'Z', 'Z', 'Z']}
        dunt_71 = CabinetMaker(args, login=False, host="localhost", port=2000, tls=False)
        dunt_71.fce = 'product'
        dunt_71.add_side_left(info=None, area_id=None, mat=None, pos=None, diff=None, save=True, size=None)
        dunt_71.add_side_right(info=None, area_id=None, mat=None, pos=None, diff=[0, 0, 0, 0, 0, 400], save=True, size=None)
        dunt_71.add_top(info=None, area_id=None, mat=None, bars_width=None, pos=None, diff=[0, 400, 0, 0, 0, 0], save=True, size=None)
        dunt_71.add_base(info=None, area_id=None, mat=None, diff=None, save=True, size=None)
        dunt_71.add_dividers(info=None, area_id=None, array_dist=[1, 18], mat=None, part_size=None, thickness=None, diff=None, part=False, save=True, typ='B', areas=True)
        dunt_71.add_dividers(info=None, area_id=1, array_dist=[1, 400], mat=None, part_size=None, thickness=None, diff=[18, 0, 0, 0, 0, 0], part=False, save=True, typ='C', areas=True)
        dunt_71.add_element(area_id=3, mat=None, joints=None, number=None, pos=None, diff=None, typ='B', size=[580, 510, 18], info=None, size_override=False, name=None, rot=[0, -45, 0], edge=None, shape_contour=None, save=True)
        dunt_71.add_doors(area_id=None, handleHeight='DOWN', handle=True, mat=None, handleSize=[160, 25, 5], stacking='HORIZONTAL', number=1, door_type='AUTOMAT', diff=None, pars_front=[3, 3, 3, 3, 3], handleSide=None, info=None, style='FLAT', grains=True, post_diff=None, handleOrientation='HORIZONTAL', save=True, handlePos=[50, 50])
        dunt_71.add_shelve(info=None, area_id=None, mat=None, number=[400, 1], diff=None, rotation=None, save=True, size=None)
        dunt_71.add_empty(func_key='add_shape_cut', origin=2, tool_side='center', number=4, pos=None, joint='add_shape_cut_diag', shape=True, x_dist=400, tool_side_close='center', rot=None, size=None, tool_diameter=10, index=5, y_dist=400, process_type='acamProcessROUGH_FINISH', tool_number=1, final_depth=0, planes=None, save=True)
        dunt_71.finish()
    
    def test_closer():
        args = {'edgeSIDE': ['Z', 0, 0, 0], 'thickConstr': 18, 'frontOut': False, 'socle': 0, 'matSteel': 'F509', 'matBack': '101', 'size': [2000, 600, 2000], 'style': 'FLAT', 'thickDrawer': 18, 'thickBack': 5, 'edgeDRAWER': ['X', 0, 0, 0], 'frame_width': 70, 'edgeTOP': ['Z', 0, 0, 0], 'matConstr': 'H3702', 'edges': True, 'elementInfo': {'fittings': {'KOL': 5}, 'production': {'EDGEBANDER': 2, 'HAND': 3, 'SAW': 1, 'COATING': False, 'CNC': 1}, 'group': 'dunt_77', 'visibility': 'NORMAL', 'block': True}, 'rotation': [0, 0, 0], 'matFront': 'H3702', 'product_type': 'product', 'name': 'dunt_77', 'position': [0, 0, 0], 'edgeDOOR': ['Z', 'Z', 'Z', 'Z']}
        dunt_77 = CabinetMaker()
        dunt_77.fce = 'product'
        dunt_77.add_bar(area_id=None, diff_Z=False, mat=None, diff_X=True, bar_width='X', locations=[0, 1], bar_length='Z', diff=[18, 18, 0, 0, 0, 0], size=120, info=None, name=None, grains=True, diff_Y=True, edge=None, post_diff=None, save=True)
        dunt_77.add_side_left(info=None, area_id=None, mat=None, pos=None, diff=None, save=True, size=None)
        dunt_77.add_side_right(info=None, area_id=None, mat=None, pos=None, diff=None, save=True, size=None)
        dunt_77.add_bar(area_id=None, diff_Z=False, mat=None, diff_X=False, bar_width='Y', locations=[0, 1], bar_length='X', diff=None, size=120, info=None, name=None, grains=True, diff_Y=True, edge=None, post_diff=None, save=True)
        dunt_77.add_dividers(info=None, area_id=None, array_dist=[5, 4, 5, 4, 5], mat=None, part_size=None, thickness=None, diff=None, part=True, save=True, typ='B', areas=True)
        dunt_77.add_shelve(info=None, area_id=[1, 3], mat=None, number=None, diff=None, rotation=None, save=True, size=None)
        dunt_77.add_dividers(info=None, area_id=[2], array_dist=[1, 1], mat=None, part_size=None, thickness=None, diff=None, part=True, save=True, typ='C', areas=True)
        dunt_77.add_dividers(info=None, area_id=[0], array_dist=[8, 1], mat=None, part_size=None, thickness=None, diff=None, part=True, save=True, typ='C', areas=True)
        dunt_77.add_dividers(info=None, area_id=[4], array_dist=[9, 9, 2], mat=None, part_size=None, thickness=None, diff=None, part=True, save=True, typ='C', areas=True)
        dunt_77.add_shelve(info=None, area_id=[6], mat=None, number=None, diff=None, rotation=None, save=True, size=None)
        dunt_77.add_drawers(info=None, area_id=5, save=True, handle=True, mat=None, grains=True, number=None, drawer_type='AUTOMAT', diff=None, pars_front=[3, 3, 39, 3, 3], mat_front=None, pars_in=[12, 12, 0, 40, 10, 40])
        dunt_77.add_doors(area_id=None, handleHeight='TOP', handle=False, mat=None, handleSize=[160, 25, 5], stacking='HORIZONTAL', number=[4, 3, 4], door_type='INSIDE', diff=[0, 0, -80, 0, 18, 18], pars_front=[3, 3, 3, 3, 3], handleSide=None, info=None, style='FLAT', grains=True, post_diff=None, handleOrientation='VERTICAL', save=True, handlePos=[50, 50])
        dunt_77.add_del_element(index=-2, save=True)
        dunt_77.add_doors(area_id=None, handleHeight='TOP', handle=False, mat=None, handleSize=[160, 25, 5], stacking='HORIZONTAL', number=[3, 4, 3], door_type='INSIDE', diff=[0, 0, -140, 0, 18, 18], pars_front=[3, 3, 3, 3, 3], handleSide=None, info=None, style='FLAT', grains=True, post_diff=None, handleOrientation='VERTICAL', save=True, handlePos=[50, 50])
        dunt_77.add_del_element(index=[-1, -3], save=True)
        dunt_77.finish()

    
    def test_count_base_elements():
        con = CabinetMaker(host="localhost", port=2000, tls=False, args=None, login=False)
        products = con.get_products_all()
        count = 0
        for prod in products.products:
            prod = AttrDict(prod)
            if prod.fce != "item":
                for name, element in prod.elements.items():
                    if name in prod.names['base']:
                        element = AttrDict(element)
                        pos = [x + y for x, y in zip(element.elementPosition, element.product_position)]
                        if 50 < pos[2] <= 150:
                            count += 4
        ret = con.action(url="/db/nozicky/append")
        ret = con.action(url="/products/db_nozicky/edit", data={"quantity":count}, method="POST")
        pass
    # test_count_base_elements()



