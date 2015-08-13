def setup():
			global system
			try:
				import sys
				sys.path.insert(0,'.')
				from system import TQD
				system = TQD('params.py')
			except Exception as e:
				system = e
			return 0