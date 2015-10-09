###############################################################################
##  Bisquik                                                                  ##
##  Center for Bio-Image Informatics                                         ##
##  University of California at Santa Barbara                                ##
## ------------------------------------------------------------------------- ##
##                                                                           ##
##     Copyright (c) 2007 by the Regents of the University of California     ##
##                            All rights reserved                            ##
##                                                                           ##
## Redistribution and use in source and binary forms, with or without        ##
## modification, are permitted provided that the following conditions are    ##
## met:                                                                      ##
##                                                                           ##
##     1. Redistributions of source code must retain the above copyright     ##
##        notice, this list of conditions, and the following disclaimer.     ##
##                                                                           ##
##     2. Redistributions in binary form must reproduce the above copyright  ##
##        notice, this list of conditions, and the following disclaimer in   ##
##        the documentation and/or other materials provided with the         ##
##        distribution.                                                      ##
##                                                                           ##
##     3. All advertising materials mentioning features or use of this       ##
##        software must display the following acknowledgement: This product  ##
##        includes software developed by the Center for Bio-Image Informatics##
##        University of California at Santa Barbara, and its contributors.   ##
##                                                                           ##
##     4. Neither the name of the University nor the names of its            ##
##        contributors may be used to endorse or promote products derived    ##
##        from this software without specific prior written permission.      ##
##                                                                           ##
## THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS "AS IS" AND ANY ##
## EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED ##
## WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, ARE   ##
## DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR  ##
## ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL    ##
## DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS   ##
## OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)     ##
## HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,       ##
## STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN  ##
## ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE           ##
## POSSIBILITY OF SUCH DAMAGE.                                               ##
##                                                                           ##
###############################################################################
"""
SYNOPSIS
========


DESCRIPTION
===========

"""
import os
import sys
import logging
import pkg_resources
import traceback
import urlparse
import Queue
import multiprocessing
import mimetypes
import posixpath
from datetime import datetime
try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

from pyramid.view import view_config, view_defaults
#from pyramid_handlers import action
from pyramid.renderers import render_to_response
from pyramid.response import FileResponse, Response
import pyramid.httpexceptions as exc

#import tg

#from tg import config, controllers, expose, redirect, override_template
#from pylons.controllers.util import abort

#from repoze.what import predicates

#from bq.core.service import ServiceController, BaseController
from bq.util.routes import add_slash_route
from bq.exceptions import EngineError, RequestError
from bq.util.configfile import ConfigFile
from bq.util.paths import bisque_path, config_path
from bq.util.copylink import copy_link
from bq.util.abort import abort

from bq.module_engine.lib.runtime_adapter import RuntimeAdapter

log = logging.getLogger('bq.engine_service')

#
#def execone(params):
#    """ Execute a single process locally """
#    #command_line, stdout = None, stderr=None, cwd = None):
#    #print "Exec", params
#    command_line = params['command_line']
#    rundir = params['rundir']
#
#    if os.name=='nt':
#        exe = which(command_line[0])
#        exe = exe or which(command_line[0] + '.exe')
#        exe = exe or which(command_line[0] + '.bat')
#        if exe is None:
#            raise RunnerException ("Executable was not found: %s" % command_line[0])
#        command_line[0] = exe
#    print 'CALLing %s in %s' % (command_line,  rundir)
#    return subprocess.call(params['command_line'],
#                           stdout = open(params['logfile'], 'a'),
#                           stderr = subprocess.STDOUT,
#                           shell  = (os.name == "nt"),
#                           cwd    = rundir,
#                           )

def method_unavailable (msg=None):
    raise exc.exception_response(503)

def method_not_found():
    raise exc.HTTPNotFound()

def server_unavailable ():
    raise exc.exception_response(503)

def illegal_operation(msg=None):
    raise exc.exception_response(501, comment=msg)

def read_xml_body(request):
    "Read the xml body from a TG request"
    clen = request.content_length
    content = request.content_type
    if content.startswith('text/xml') or content.startswith('application/xml'):
        return etree.XML(request.body)
    return None

def load_module(module_path, engines = None, settings = None):
    """load a module XML file if enabled and available

    :param module_path: path to module.xml
    :param engines: A dict of engine adapters i.e.
    """
    module_name = os.path.basename (module_path)
    module_dir = os.path.dirname (module_path)
    cfg = os.path.join(module_dir, 'runtime-module.cfg')
    if not os.path.exists(cfg):
        log.debug ("Skipping %s (%s) : no runtime-module.cfg" , module_name, cfg)
        return None
    cfg = ConfigFile (cfg)
    mod_vars = cfg.get (None, asdict = True)
    enabled = mod_vars.get('module_enabled', 'true').lower() == "true"
    #status = (enabled and 'enabled') or 'disabled'
    if not enabled :
        log.debug ("Skipping %s : disabled" , module_name)
        return None
    ### Check that there is a valid Module descriptor
    if not os.path.exists(module_path):
        return None
    log.debug ("found module at %s" , module_path)
    try:
        with open(module_path) as xml:
            module_root = etree.parse (xml).getroot()
    except etree.XMLSyntaxError:
        log.exception ('while parsing %s', module_path)
        return None
    bisque_cfg = os.path.join(module_dir,'runtime-bisque.cfg')

    #if  os.path.exists(bisque_cfg):
    #    os.unlink (bisque_cfg)
    copy_link (config_path('runtime-bisque.cfg', settings=settings), bisque_cfg)

    ts = os.stat(module_path)
    # for elem in module_root:
    if module_root.tag == "module":
        module_name = module_root.get('name')
        module_path = module_root.get('path')
        module_type = module_root.get('type')
        module_root.set('ts', datetime.fromtimestamp(ts.st_mtime).isoformat())
        engine = engines and engines.get(module_type, None)
        if engine and not engine.check (module_root):
            return None
        #module_root.set('value', engine_root + '/'+module_name)
        #module_root.set('value', "%s/%s" % (settings['bisque.engine_root'] , module_name))
        module_root.set('value', "%s" %  module_name)
        #module_root.set('status', status)
        #for x in module_root.iter(tag=etree.Element):
        #    x.set('permission', 'published')
        module_root.set ('dirpath', module_dir)
        return module_root
    return None



def initialize_available_modules(engines, settings):
    '''Load a local directory with installed modules.

    Return a list of loaded module xml descriptors
    '''
    available = []
    unavailable = []

    MODULE_PATH = settings.get('bisque.engine_service.local_modules', bisque_path('modules', settings=settings))


    log.debug ("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
    log.debug ('examining %s ' , MODULE_PATH)
    log.debug ("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
    for g in os.listdir(MODULE_PATH):
        module_path = os.path.join(MODULE_PATH, g, g + '.xml')
        module_root = load_module(module_path, engines, settings=settings)
        if module_root is not None:
            available.append(module_root)
        else:
            unavailable.append ( g )
            log.debug("Skipping %s : engine_check failed" , g)

    return available, unavailable

#################################################################
##
#@view_defaults(route_name='module_engine')

class BQUtil(object):
    def __init__(self,request):
        self.request = request
    def url(self, x):
        return x
    def get(self, name, default):
        return self.request.registry.settings.get (name, default)





def engine_bootstrap (request):
    #log.info ("BOOTSTRAP settings %s", request.registry.settings)

    root = EngineRoot(request.registry.settings['engine.modules'], request.registry.settings['engine.unavailable'])
    return root





class EngineRoot (object):
    __name__ = ""
    __parent__  = None

    def __init__ (self, modules, unavailable):
        self.modules = {}
        self.status = "free"
        self.jobs = 0
        self.running = {}
        self.module_by_name = {}
        self.resource_by_name = {}

        if os.name == 'nt':
            sys.argv = [sys.argv[0].replace('paster-script.py', 'python.exe'), 'bqengine\\bq\\engine\\controllers\\execone.py']
            import execone
            sys.modules['__main__'] = execone
            from multiprocessing.forking import set_executable
            set_executable( sys.argv[0].replace('paster-script.py', 'python.exe') )
            sys.argv[1] = 'bqengine\\bq\\engine\\controllers\\execone.py'
            del sys.argv[2:]

        #self.mpool = multiprocessing.Pool(POOL_SIZE)

        #self.module_resource = EngineResource()
        self.unavailable = unavailable
        self.modules = dict ( (m.get('name'), m) for m in modules )
        for module in modules:
            #self.module_resource[module.get('name')] =  EngineModuleResource(module, None))
            self.module_by_name[module.get('name')]  = module


    def __getitem__(self, name):
        log.info ("ROOT: %s", name)

        module = self.module_by_name[name]
        return module


class EngineServer(object):
    """Engine server : provide web access to analysis modules
    """
    __name__ = "engine_service"
    __parent__  = None

    def __init__(self, context, request):
        self.context = context
        self.request = request
        log.info ("Engine (%s, %s) context %s request %s", self.__name__, self.__parent__, context, request)



    #@expose('bq.engine.templates.engine_modules')
    #@view_config ('index', renderer="'bq.module_engine.templates.engine_modules")
    @view_config(route_name='engine_index', renderer='bq.module_engine.templates:engine_modules.genshi')
    @view_config(route_name='engine_index1', renderer='bq.module_engine.templates:engine_modules.genshi') #allows for '/' and '/index'
    #@view_config(route_name='engine_shortcut', renderer='bq.module_engine.templates:engine_modules.genshi')
    #@action(action="",
    def index(self):
        """Return the list of available modules urls"""
        #server = urlparse.urljoin(config.get('bisque.server'), self.service_type)
        #modules = [ ("%s/%s" % (server, k), k) for k in sorted(self.module_by_name.keys())]
        #return dict(modules=modules)
        log.info ("ENGINE_INDEX")
        reload_modules (self.request.registry.settings)
        modules = self.request.registry.settings['engine.modules']

        #return dict(urls = [ (self.request.current_route_url (m.get('name')), m.get ('name')) for m in modules.values()], bq = BQUtil (self.request))
        return dict(urls = [ (('/'+self.__name__+'/'+m.get('name')), m.get ('name')) for m in modules.values()], bq = BQUtil (self.request)) #allows for the resource to be independent of the url

    #@expose(content_type="text/xml")
    @view_config (route_name='engine_service',  renderer='xml')
    def _services(self):
        module_by_name = self.request.registry.settings['engine.modules']
        log.info ("_services : %s" , module_by_name.keys())
        resource = etree.Element('resource')
        rooturl = posixpath.dirname (self.request.current_route_url())
        for m in module_by_name.values():
            etree.SubElement(resource, 'service', name=m.get('name'), value=posixpath.join (rooturl, m.get('value')))
        return etree.tostring (resource)

    ##@expose(content_type="text/xml")
    #def _default(self, *path, **kw):
    #    log.debug ('in default %s' % str( path) )
    #    path = list(path)
    #    if len(path) > 0:
    #        module_name = path.pop(0)
    #        if module_name in self.unavailable:
    #            method_unavailable("Module is disabled")
    #    method_not_found()



##################################################################################
##
reserved_io_types = ['system-input']

#from tg import require
#from repoze.what.predicates import not_anonymous
#from bq.config.app_cfg import public_file_filter

#@view_defaults (http_cache = 60)
class EngineModuleResource(object):
    """Convert the local module into one accessable as a web resource"""
    __name__ = "Module"
    __parent__  = None



    adapters = {
        #'matlab': MatlabAdapter(),
        #'python': PythonAdapter(),
        #'shell' : ShellAdapter(),
        'runtime' : RuntimeAdapter,
    }

    def filepath(self, *path):
        log.debug('name %s, path %s', self.name,path)
        #return bisque_path('modules',self.name,  *path)
        return os.path.join (self.module_path, *path)

    def __init__(self, request):
        log.info ("ModuleResource __init__ ", )
        self.request = request
        module_name = self.request.matchdict.get ('module_name')

        if module_name:
            log.info("interface %s" % module_name)
            self.module_xml = self.request.registry.settings['engine.modules'].get (module_name)
            if not self.module_xml:
                log.error ('no %s in module ', module_name)
                abort (404)

            self.module_uri = self.module_xml.get('uri')
            self.name = module_name
            self.module_path  =  bisque_path('modules', self.name)
            self.define_io() # this should produce lists on required inputs and outputs

    def serve_entry_point(self, node, default='Entry point was not found...', content_type='text/html', **kw):
        """Provide a general way to serve an entry point"""

        #from pylons.controllers.util import forward
        #from paste.fileapp import FileApp

        if isinstance(node, str) is True:
            node = self.module_xml.findall(node)

        text = default
        if  len(node): # Found at least one xpath match
            node = node[0]
            type = node.get('type', None)
            if type == 'file':
                path = self.filepath(node.get('value'))
                log.debug('path %s exists %s', path, os.path.exists(path))
                if os.path.exists(path):
                    if content_type is None:
                        content_type, encoding  = mimetypes.guess_type (path, strict=False)
                    #return forward(FileApp(path).cache_control (max_age=60*60*24*7*6))
                    return FileResponse(path, content_type=content_type, cache_max_age =60*60*24*7*6)

            else:
                text = node.get ('value', None)
                if node.get ('value', None) is None:
                    # Using a <value><![CDATA]</value>
                    text = (node[0].text)

        if text is None:
            abort(404)
        return Response(text, content_type=content_type, cache_expires=60)


    def definition_as_dict(self):
        def _xml2d(e, d, path=''):
            for child in e:
                name  = '%s%s'%(path, child.get('name', ''))
                ttype = child.get('type', None)
                value = child.get('value', None)
                if value is not None:
                    if not name in d:
                        d[name] = value
                    else:
                        if isinstance(d[name], list):
                            d[name].append(value)
                        else:
                            d[name] = [d[name], value]
                    #if not ttype is None:
                    #    d['%s.type'%name] = ttype

                d = _xml2d(child, d, path='%s%s/'%(path, child.get('name', '')))
            return d

        d = _xml2d(self.module_xml, {})
        d['module/name'] = self.name
        d['module/uri']  = self.module_uri
        if not 'title' in d: d['title'] = self.name
        return d



#    <tag name="inputs">
#        <tag name="image_url"    type="image" />
#        <tag name="resource_url" type="resource">
#            <tag name="template" type="template">
#                <tag name="type" value="image" />
#                <tag name="type" value="dataset" />
#                <tag name="selector" value="image" />
#                <tag name="selector" value="dataset" />
#            </tag>
#        </tag>
#        <tag name="mex_url"      type="system-input" />
#        <tag name="bisque_token" type="system-input" />
#    </tag>
#
#    <tag name="outputs">
#         <tag name="MetaData" type="tag" />
#         <gobject name="Gobjects" />
#    </tag>


    def define_io(self):

        def define_tempalte(xs):
            l = []
            for i in xs:
                r = i.tag
                n = i.get('name', None)
                v = i.get('value', None)
                t = i.get('type', None)
                if t in reserved_io_types: continue
                x = { 'resource_type': r, 'name': n, 'value': v, 'type': t, }

                #tmpl = i.xpath('tag[@name="template" and @type="template"]/tag')
                tmpl = i.findall("tag[@name='template']/tag")
                for c in tmpl:
                    nn = c.get('name', None)
                    vv = c.get('value', None)
                    if not nn in x:
                        x[nn] = vv
                    else:
                        if isinstance(x[nn], list):
                            x[nn].append(vv)
                        else:
                            x[nn] = [x[nn], vv]
                #if 'label' not in x: x['label'] = n
                l.append(x)
            return l

        self.inputs  = define_tempalte( self.module_xml.findall("./tag[@name='inputs']") )
        self.outputs = define_tempalte( self.module_xml.findall("./tag[@name='outputs']") )
        log.debug("Inputs : %s", self.inputs)
        log.debug("Outputs: %s", self.outputs)


    #@expose()
    @view_config(route_name='module_index', renderer='string')
    @view_config(route_name="module_interface", renderer='string')
    #@action()
    def index(self, **kw):
        """Return interface of the Module

        A default interface will be generate if not defined by the
        module itself.
        """
        log.info("index %s" % self.name)

        node = self.module_xml.findall("./tag[@name='interface']")
        log.debug('Interface node: %s '%node)
        #if not node or not node[0].get('value', None):
            #override_template(self.index, "genshi:bq.engine.templates.default_module")

        module_def_dict = self.definition_as_dict()
        js = module_def_dict.get('interface/javascript',[])
        css = module_def_dict.get('interface/css',[])
        template = module_def_dict.get('interface', None)
        if isinstance(js, str):
            module_def_dict['interface/javascript'] = [js]
        else:
            module_def_dict['interface/javascript'] = js
        if isinstance(css, str):
            module_def_dict['interface/css'] = [css]
        else:
            module_def_dict['interface/css'] = css
        log.debug('module_def_dict: %s'%module_def_dict)
        template_path = "bq.module_engine.templates:default_module.genshi"
        if isinstance(template, str):
            template_path = self.filepath(template)
        log.debug('template path: %s',template_path)
        response = render_to_response(template_path,
                                      dict (module_uri  = self.module_uri,
                                            module_name = self.name,
                                            module_def  = module_def_dict,
                                            module_xml  = etree.tostring(self.module_xml),
                                            bq = BQUtil(self.request),
                                            inputs  = self.inputs,
                                            outputs = self.outputs,
                                            extra_args  = kw
                                        ),
                                      self.request)
        response.cache_expires = 60
        return response
        #return self.serve_entry_point(node)

    #@expose()
#    @view_config(route_name="module_interface", renderer='string')
#    def interface(self, **kw):
#        """Provide Generate a module interface to be used"""
#        node = self.module_xml.findall('./tag[@name="interface"]')
#        log.debug('Interface node: %s'%node)
#        if not node or not node[0].get('value', None): #check if interface has a
#            #override_template(self.interface, "genshi:bq.engine.templates.default_module")
#            response = render_to_response("../templates/default_module.genshi",
#                                      dict (module_uri  = self.module_uri,
#                                            module_name = self.name,
#                                            module_def  = self.definition_as_dict(),
#                                            module_xml  = etree.tostring(self.module_xml),
#                                            inputs  = self.inputs,
#                                            outputs = self.outputs,
#                                            bq = BQUtil(self.request),
#                                            extra_args  = kw),
#                                         self.request)
#            response.cache_expires = 60
#            return response
#
#
#
#        return self.serve_entry_point(node)

    #@expose()
    @view_config(route_name="module_help", renderer='string')
    def help(self, **kw):
        """Return the help of the module"""
        help_text =  "No help available for %s" % self.name
        return self.serve_entry_point('./tag[@name="help"]', help_text, content_type='text/html')

    #@expose()
    @view_config(route_name="module_thumbnail")
    def thumbnail(self, **kw):
        """Return the thumbnail of the module"""
        return self.serve_entry_point('./tag[@name="thumbnail"]', 'No thumbnail found', content_type=None)

    #@expose()
    @view_config(route_name="module_description")
    def description(self, **kw):
        """Return the textual desfription of the module"""
        return self.serve_entry_point('./tag[@name="description"]', 'No description found', content_type='text/html')

    #@expose(content_type="text/xml")
    @view_config(route_name="module_definition", renderer="xml")
    #@action(renderer='string')
    def definition(self, **kw):
        # rewrite stuff here for actual entry points
        return self.module_xml

    #@expose()
    def status (self):
        """Return  executions of the Module"""

    #@expose()
    @view_config(route_name="module_public", renderer="string")
    def public(self, **kw):
        """Deliver static content for the Module"""
        log.debug ("in Static %s %s" % (str(self.request.matchdict.get('path')), str(kw)))

        static_path = os.path.join (self.module_path, 'public', *self.request.matchdict.get('path',()))
        log.debug('static_path %s'%static_path)
        try:
            return FileResponse(static_path, cache_max_age =60*60*24*7*6)
            #cont = open(static_path)
            #return cont.read()
        except IOError:
            log.debug('Static File Not Found')
            abort(404)


#    def create(self, **kw):
#        """Used by new for the factory"""
#        return ""

#    def new(self, factory, xml, **kw):
#        """Start an execution a new execution"""
#        #
#        mex = etree.XML(xml)
#        log.debug ("New execution of %s" % etree.tostring(mex))
#        mex = self.start_execution(mex)
#        response =  etree.tostring(mex)
#        log.debug ("return %s " % response)
#        return response

    def get(self, resource, **kw):
        """Return the interface of the  specified module execution"""

    def append(self, resource, xml, **kw):
        """Send new data the specified module execution"""


    #@expose(content_type='text/xml')
    #You cannot require a valid login on the engine .. there are no users here!
    #@require(not_anonymous(msg='You need to log-in to run a module'))
    #@action(request_method = 'POST')
    @view_config(route_name="module_execute", renderer="string", request_method = 'POST')
    def execute(self, entrypoint = 'main'):
        """Start an module execution with a mex
        """
        log.debug("execute %s" % self.name)
        mex = read_xml_body(self.request)
        if mex is not None:
            log.debug ("New execution of %s" % etree.tostring(mex))
            response = self.start_execution(mex)
            log.debug ("return %s " % response)
            return response
        else:
            illegal_operation("No Mex Body found")

    def start_execution(self, mextree):
        """Start the execution of the mex for this module"""
        b, mexid = mextree.get ('uri').rsplit('/',1)
        log.debug ('engine: execute %s' % (mexid))
        module = self.module_xml
        try:
            try:
                mex_moduleuri = mextree.get ('type')
                log.debug ('moduleuri ' + str(mex_moduleuri))
                #if mex_moduleuri != module.get ('uri'):
                #    return None
                adapter_type = module.get('type')
                adapter_ctor = self.adapters.get(adapter_type, None)
                if not adapter_ctor:
                    log.error ('No adaptor for type %s' % (adapter_type))
                    raise EngineError ('No adaptor for type %s' % (adapter_type))
                adapter = adapter_ctor(self.request.registry.settings)
                exec_id = adapter.execute(module, mextree, self.request)
                mextree.append(etree.Element('tag', name='execution_id', value=str(exec_id)))
                log.info ("MODULE FINISHED")
                if mextree.get ('value') == 'FAILED':
                    self.request.response.status_int = 500

                #if not mextree.get ('asynchronous'):
                #    mextree.set('status', "FINISHED")

            except EngineError, e:
                log.exception ("EngineError")
                mextree.set('value', 'FAILED')
                mextree.append(etree.Element('tag', name='error_message', value=str(e)))
                self.request.response.status_int = 500

            except (KeyboardInterrupt, SystemExit):
                raise

            except :
                log.exception ("UNKNOWN Exception in adaptor:" )
                mextree.set('value', 'FAILED')
                excType, excVal, excTrace  = sys.exc_info()
                trace =  " ".join(traceback.format_exception(excType,excVal, excTrace))
                mextree.append (etree.Element ('tag',name='error_message', value=str(trace)))
                self.request.response.status_int = 500
        except:
            log.exception ("BEFORE FINALLY")

        finally:
            self.request.response.body = etree.tostring(mextree, pretty_print=True)
            return self.request.response

########################################################################
# rload
def reload_modules (settings):
    engines = { #'matlab': MatlabAdapter(),
        #'python': PythonAdapter(),
        #'shell' : ShellAdapter(),
        #'runtime' : RuntimeAdapter(),
        #'lam' : LamAdapter(),
        }

    module_load = settings.get('engine.module_dir_mtime', None)
    if module_load:
        if module_load >= os.stat ( settings['bisque.engine_service.local_modules'] ).st_mtime:
            return
    log.debug ("loading modules")
    modules, unavailable = initialize_available_modules(engines, settings=settings)
    #log.debug ('found modules= %s' % str(modules))
    #settings['engine.modules'] = modules
    settings['engine.modules'] =  dict((m.get('name'), m) for m in modules)
    settings['engine.unavailable'] = unavailable
    settings['bisque.engine_service.local_modules'] =  bisque_path('modules', settings=settings)
    log.info ("ENGINE.MODULES = %s", settings['engine.modules'])
    settings['engine.module_dir_mtime'] = os.stat ( settings['bisque.engine_service.local_modules'] ).st_mtime




#########################################################################
# Initialization
def engine_config (config):
    log.info("engine config")
    settings = config.get_settings()
    poolsize =  int (settings.get('bisque.engine_service.poolsize', 4))
    settings['bisque.engine_root']  = '/'.join ([settings.get('bisque.server','') , 'engine_service'])

    reload_modules(settings)
    config.add_route('engine_index', '/')
    config.add_route('engine_index1', '/index')
    config.add_route('engine_service', '/_services')
    add_slash_route(config, 'module_index', '/{module_name}/')
    config.add_route('module_help', '/{module_name}/help')
    config.add_route('module_thumbnail', '/{module_name}/thumbnail')
    config.add_route('module_interface', '/{module_name}/interface')
    config.add_route('module_description', '/{module_name}/description')
    config.add_route('module_definition', '/{module_name}/definition')
    config.add_route('module_execute', '/{module_name}/execute')
    config.add_route('module_public', '/{module_name}/public*path')

    if os.name == 'nt':
        from bq.module_engine.lib import execone
        path = os.path.abspath(execone.__file__)
        sys.argv = [sys.argv[0].replace('paster-script.py', 'python.exe'), '%s\\execone.py'%path]
        sys.modules['__main__'] = execone
        from multiprocessing.forking import set_executable
        set_executable( sys.argv[0].replace('paster-script.py', 'python.exe') )
        sys.argv[1] = '%s\\execone.py'%path
        del sys.argv[2:]
    # At some point reanable this
    #settings['engine.mpool'] = multiprocessing.Pool(pool_size)
    config.scan ('bq.module_engine.controllers.engine_service')

includeme = engine_config

#from bq.module_engine.lib.mex_authorization import MexAuthAuthenticationPolicy


def initialize(request):
    """ Initialize the top level server for this microapp"""
    log.info ("engine initialize ")
    service =  EngineServer(request)
    return service

#def get_static_dirs():
#    """Return the static directories for this server"""
#    package = pkg_resources.Requirement.parse ("bisque_engine")
#    package_path = pkg_resources.resource_filename(package,'.')
#    return [(package_path, os.path.join(package_path, 'bq', 'engine', 'public'))]

#def get_model():
#    from engine import model
#    return model

__controller__ =  EngineServer
