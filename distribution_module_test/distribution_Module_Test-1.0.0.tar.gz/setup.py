#从python发布工具导入 setup 函数
from distutils.core import setup

#以下是setup函数以及它的参数列表, setup的参数即模块的元数据
setup(
	name			= 'distribution_Module_Test',
	version			= '1.0.0',
	py_modules 		= ['distribution_Module_Test'],#这是一个模块列表
	author			= 'taomidashi',
	author_email	= 'taomidashi@126.com',
	url				= 'http://taomidashi.com',
	description		= '模块发布测试'
	)