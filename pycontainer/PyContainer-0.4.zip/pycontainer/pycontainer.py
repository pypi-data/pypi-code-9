'''
PyContainer -- a simple IoC (Dependency Injection) lightweight
container for Python.
'''

from __future__ import nested_scopes
import sys
import utils
import objectify
import interceptors

__version__ = "0.4"
__author__ = "Rafal Sniezynski"

class PyContainer(object):
	'''The IoC container class.'''
	def __init__ (self, config=None, parent=None, register=0):
		'''
		@param config: XML config file path (optional, if absent, configXml must be later invoked)
		@type config: String
		@param parent: a parent container (optional)
		@type parent: PyContainer
		@param register: if True, child container is registered in parent container for lifecycle management purposes
		@type register: bool
		'''
		if parent is None: self.parent = None
		else:
			self.parent = parent
		self.children = []
		self.descriptions, self.classes,  self.instances, self.factories = {}, {}, {}, {}
		factoriesFileName = ""
		if register and self.parent:
			self.parent.children.append(self)
		if config: self.configXml(config)
		
	def configXml (self, name):
		'''
		Reads the container wiring description from an XML file of a given name
		and initializes the container.
		@type name: String
		@param name: name of the XML config file
		'''
		self.config = objectify.instance(name)
		self.factoriesFileName = getattr(self.config, "factories", "")
		for componentDesc in self.config.component:
			id_ = componentDesc.id
			klass = getattr(componentDesc, "class")
			comp = _Component(id_, klass)
			comp.factoryId = getattr(componentDesc, "factory", "default")
			comp.type_ = getattr(componentDesc, "type", _Component.SINGLETON)

			# Add properties to component description:
			for propertyDesc in getattr(componentDesc, "property", []):
				prop = _Property(propertyDesc.name)
				if hasattr(propertyDesc, "local"):
					prop.local = propertyDesc.local
					prop.type_ = _Property.LOCAL
				else:
					prop.value = eval(propertyDesc.PCDATA.strip(), {})
					prop.type_ = _Property.VALUE
				comp.addProperty(prop)

			# Add interceptors to component description:
			for interceptorDesc in getattr(componentDesc, "interceptor__ref", []):
				comp.addInterceptor(interceptorDesc.name)
				
			self.descriptions[id_] = comp
			self.classes[id_] = klass
		self.__createFactories()
		self.__verify()

	def __verify (self):
		'''
		Verifies the wiring of the components.
		'''
		parentDescriptions = {}
		if self.parent:
			parentDescriptions = self.parent.descriptions.copy()
		parentDescriptions.update(self.descriptions)
		for comp in parentDescriptions.values():
			for prop in comp.properties:
				if hasattr(prop, "local"):
					if not parentDescriptions.has_key(prop.local):
						raise AttributeError, "Configuration error, referenced component %s doesn't exist" %prop.local

	def __createFactories (self):
		'''
		Creates instances of the factories defined in (optional) factories file.
		'''
		if self.factoriesFileName:
			factoriesFile = objectify.instance(self.factoriesFileName)
			for factory in factoriesFile.factory:
				factoryInstance = utils.getClass(getattr(factory, "class"))()
				# Inject properties to the factory instance:
				for property in getattr(factory, "property", []):
					name = property.name
					value = eval(property.PCDATA.strip(), {})
					setattr(factoryInstance, name, value)
				self.factories[factory.id] = factoryInstance
		if not self.factories.has_key("default"):
			self.factories["default"] = utils.getClass("pycontainer.factories.LocalFactory")()
		

	def getInstance (self, id_):
		'''
		Returns an instance of a component. This method performs
		lazy instantiation - only components required for this component to
		be initialized properly are instantinated.
		@type id_: String
		@param id_: same thing as the 'id' attribute in the XML config file.
		@rtype: user-specified
		@return: an object of a class specified in config
		'''
		if self.classes.has_key(id_):
			if self.descriptions[id_].type_ == _Component.PROTOTYPE:
				if not self.instances.has_key(id_):
					self.instances[id_] = _Instance()
				instance = self.factories[self.descriptions[id_].factoryId].getInstance(self.classes[id_])
				if self.descriptions[id_].interceptors:
					instance = _Invocation(self, id_, instance)  # Wrap the instance
				self.instances[id_].private.append(instance)
				self.__updateInstanceProperties(id_)
				return instance

			else:
				if not self.instances.has_key(id_):
					self.instances[id_] = _Instance()
					instance = self.factories[self.descriptions[id_].factoryId].getInstance(self.classes[id_]) # !!!
					if self.descriptions[id_].interceptors:
						instance = _Invocation(self, id_, instance)  # Wrap the instance
					self.instances[id_].singleton = instance
					self.__updateInstanceProperties(id_)
					return instance
				else:
					return self.instances[id_].singleton

		elif self.parent:
			return self.parent.getInstance(id_)
		else:
			return None  # raise an exception?
		

	def __getitem__ (self, id_):
		'''
		Allows dictionary-like access to instances, calls
		getInstance(id_)
		@type id_: String
		@param id_: same thing as the 'id' attribute in the XML config file.
		@rtype: user-specified
		@return: an object of a class specified in config
		'''
		return self.getInstance(id_)

	def __updateInstanceProperties (self, classname):
		'''
		Updates properties of a newly created instance (recursively, if necessary).
		'''
		instances = self.instances[classname].all
		properties = self.descriptions[classname].properties
		interceptors = self.descriptions[classname].interceptors
		for instance in instances:
			for property in properties:
				# If component has interceptors, unwrap the instance from the _Invocation object:
				if isinstance(instance, _Invocation):
					instance = instance._Invocation__instance
				if property.type_ == _Property.VALUE:
					setattr(instance, property.name, property.value)
				elif property.type_ == _Property.LOCAL:
					setattr(instance, property.name, self.getInstance(property.local))

	def __getInstanceIdsInDependencyOrder (self):
		checked = {}
		instanceIds = []
		def checkInstance (id_):
			locals_ = self.descriptions[id_].getLocals()
			if checked.has_key(id_): return  # Already processed
			elif not locals_:  # Independent
				instanceIds.append(id_)
				checked[id_] = 1
			else:
				for local in locals_:
					# If circular depenedncy:
					if self.instances.has_key(local) and (id_ in self.descriptions[local].getLocals()):
						continue
					elif self.instances.has_key(local) and not checked.has_key(local):
						checkInstance(local)
				instanceIds.append(id_)
				checked[id_] = 1
		for id_ in self.instances.keys():
			checkInstance(id_)
		return instanceIds

	def start (self):
		self.method("start", order=1)

	def stop (self):
		self.method("stop", order=0)

	def dispose (self):
		self.method("dispose", order=0)

	def method (self, name, args=None, kwargs=None, order=1):
		if not order:
			for child in self.children: child.method(name, args, kwargs, order)
		if args is None: args = []
		if kwargs is None: kwargs = {}
		ordr = self.__getInstanceIdsInDependencyOrder()
		if not order:
			ordr.reverse()
		for id_ in ordr:
			instances = self.instances[id_].all
			for instance in instances:
				if hasattr(instance, name) and callable(getattr(instance, name)):
					getattr(instance, name)(*args, **kwargs)
		if order:
			for child in self.children: child.method(name, args, kwargs, order)

	def __str__ (self):
		output = []
		for id_, instance in self.instances.items():
			output.append(id_+": "+ str(instance))
		return "\n".join(output)
	
class _Component(object):
	'''Represents a component description with its properties.
	This class should only be used internally by PyContainer.'''
	SINGLETON = "singleton"
	PROTOTYPE = "prototype"
	def __init__(self, id_, klass):
		'''id_ - component id, an "interface", klass - classpath (modulepath-dot-classname)'''
		self.id_ = id_
		self.klass = klass
		self.properties = []
		self.interceptors = []

	def addProperty (self, property):
		'''Adds a property to component property list.'''
		self.properties.append(property)

	def addInterceptor (self, interceptor):
		'''Adds a interceptor to component interceptor list.'''
		self.interceptors.append(interceptor)

	def getLocals (self):
		'''Returns list of the id's of the components in the container that this component depends on.'''
		locals_ = []
		for property in self.properties:
			if property.type_ == _Property.LOCAL: locals_.append(property.local)
		return locals_
	
class _Property(object):
	'''Represents a property of a component.
	This class should only be used internally by PyContainer.'''
	LOCAL = "local"
	VALUE = "value"
	OBJECT = "object"
	def __init__ (self, name):
		self.name = name
			
class _Instance(object):
	def __init__ (self):
		self.singleton = None
		self.private = []
	def getAll (self):
		if self.singleton:
			return [self.singleton]
		else:
			return self.private
	all = property(fget=getAll)

	def __str__ (self):
		return str(self.all)
		
class _Invocation(object):
	def __init__ (self, container, id_, instance):
		self.__container = container
		self.__id = id_
		self.__instance = instance
		self.__interceptorStack = []
		for interceptorName in container.descriptions[self.__id].interceptors:
			self.__interceptorStack.append(container.getInstance(interceptorName))
		final = FinalInterceptor()
		self.__interceptorStack.append(final)

	def __getInterceptor (self):
		for interceptor in self.__interceptorStack:
			yield interceptor

	def invoke (self):
		interceptor = self.__iterator.next()
		self.call = (self.__instance, self.__methodName, self.__args, self.__kwargs)
		return interceptor.intercept(self)

	def __getattr__ (self, name):
		attr = getattr(self.__instance, name)
		if not callable(attr):
			return attr
		else:
			self.__iterator = self.__getInterceptor()
			self.__methodName = name
			return self

	def __call__ (self, *args, **kwargs):
		self.__args = args
		self.__kwargs = kwargs
		return self.invoke()

class FinalInterceptor(interceptors.Interceptor):
	'''
	Final interceptor is always at the bottom of interceptor stack.
	It executes the method.
	'''
	def intercept (self, invocation):
		instance, methodName, args, kwargs = invocation.call
		return getattr(instance, methodName)(*args, **kwargs)
