#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
在Sphinx中Member的定义包括: package, module, variable, function, class, method.
而member这个module定义了 :class:`Package` 和 :class:`Module` 两个基本类。

class, method, func, exception
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from __future__ import print_function, unicode_literals
from collections import OrderedDict
import site
import os

_root_dir = site.getsitepackages()[1]

class SubModuleNotFound(Exception):
	"""Raise when sub module/package not found.
	"""

class Package(object):
	"""Python中 ``package(包)`` 的抽象类。
	
	package必须可以被import命令所导入, 换言之, 就是已经被成功安装了。
	
	Package的属性的解释:
	
	- name: 包名称
	- parent: 母包的名称
	- subpackage: 有序字典, {子包的名称: Package对象}
	- module: 有序字典, {子模块的名称: Module对象}
	"""
	def __init__(self, name, parent=None):	
		self.name = name
		self.parent = parent
		self.subpackage = OrderedDict()
		self.module = OrderedDict()
		
		if self.parent:
			package_dir = os.path.join(
				*([_root_dir,] + self.parent.split(".") + self.name.split("."))
				)
		else:
			package_dir = os.path.join(
				*([_root_dir,] + self.name.split("."))
				)

		for basename in os.listdir(package_dir):
			abspath = os.path.join(package_dir, basename)
			
			# 如果是一个目录, 检查是否有__init__.py文件
			if os.path.isdir(abspath):
				
				# 若是一个包, 则在该目录下生成一个子包对象
				if os.path.exists(os.path.join(abspath, "__init__.py")):
					self.subpackage[basename] = Package(
						name=basename, parent=self.fullname)

			# 如果是一个文件, 检查是否是.py文件
			else:
				fname, ext = os.path.splitext(basename)
				
				# 若是一个模组, 则生成一个模组对象
				if (ext == ".py") and (fname != "__init__"):
					self.module[fname] = Module(name=fname, parent=self.fullname)
					
	@property
	def fullname(self):
		"""返回 ``package`` 的全名。
		
		全名 = 母包名.包名
		"""
		if self.parent:
			return "%s.%s" % (self.parent, self.name)
		else:
			return self.name
	
	def __str__(self):
		tpl = "Package(\n\tname='{0}', \n\tsubpackage={1}, \n\tmodule={2}, \n)"
		return tpl.format(
			self.fullname, list(self.subpackage), list(self.module))
	
	def __repr__(self):
		return self.fullname		
	
	def __getitem__(self, key):
		try:
			return self.subpackage[key]
		except KeyError:
			try:
				return self.module[key]
			except KeyError:
				raise SubModuleNotFound(
					"'%s' doesn't has sub module '%s'" % (self.name, key))
	
	def show(self, indent=0):
		"""打印包组织结构的树状图。
		"""
		def pad_text(indent):
			return "    " * indent + "|---"
		
		print("%s%s" % (pad_text(indent), self.fullname))
		
		indent += 1
		
		for p in self.subpackage.values():
			p.show(indent=indent)
		
		print("%s%s" % (pad_text(indent), self.fullname + ".__init__.py"))
		for m in self.module.values():
			print("%s%s" % (pad_text(indent), m.fullname + ".py"))
	
	def walk(self):
		"""一个迭代循环器, 返回:
		
		1. current package object (包对象)
		2. current package fullname (当前包对象的全名)
		3. all subpackage (所有子包)
		4. all submodule (所有模块)
		"""
		yield (self, self.fullname, 
			list(self.subpackage.values()), 
			list(self.module.values()),
			)
		for p in self.subpackage.values():
			for things in p.walk():
				yield things
			
class Module(object):
	"""Python中 ``module(模块)`` 的抽象类。
	
	:param name: module name
	:type name: str
	
	:param parent: default None, parent package name
	:type parent: str
	"""
	def __init__(self, name, parent=None):
		self.name = name
		self.parent = parent

	@property
	def fullname(self):
		"""返回 ``module`` 的全名。
		
		全名 = 母包名.模组名
		"""
		if self.parent:
			return "%s.%s" % (self.parent, self.name)
		else:
			return self.name

	def __str__(self):
		return "Module(name={0}, parent={1})".format(
			repr(self.name), repr(self.parent))
		
	def __repr__(self):
		return self.fullname
	
if __name__ == "__main__":
	from pprint import pprint as ppt
	import unittest
	
	class MemberUnittest(unittest.TestCase):
		"""Install requests first. https://pypi.python.org/pypi/requests
		"""
		def test_package(self):
			print("{:=^100}".format("test_package"))
			p = Package("requests")
			print(p)
			print(repr(p))
			
			for t in p.walk():
				print(t)
				
		def test_subpackage(self):
			print("{:=^100}".format("test_subpackage"))
			p = Package("requests.packages")
			print(p)
			print(repr(p))
			p.show()
		
		def test_module(self):
			print("{:=^100}".format("test_module"))
			p = Package("requests")
			m = p["api"]
 			
			print(m)
			print(repr(m))
			
	unittest.main()