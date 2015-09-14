from setuptools import setup, find_packages

packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

setup(name='app_error_handler',
      version='1.0.1',
      description='An Alternative to web application error handling',
      url='https://github.com/raviparekh/webapp-error-handler',
      author='Ravi Parekh',
      license='MIT',
      classifiers=['License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.4',
                   'Intended Audience :: Developers',
                   'Topic :: Software Development :: Libraries'],
      keywords='error-handling flask-error-handler flask django error handler',
      packages=packages,
      platforms='any',
      install_requires=['Werkzeug==0.10.4'])



