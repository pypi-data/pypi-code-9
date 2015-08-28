from distutils.core import setup
setup(
  name = 'dj_rcc',
  version = '1.0.0',
  packages = ['dj_rcc'],
  description='Redis Cluster Cache library for redis 3.0.0 built on top of redis-py-cluster',
  author = 'Piyush Chourasiya',
  author_email = 'piyushc79@gmail.com',
  maintainer='Piyush Chourasiya',
  maintainer_email='piyushc79@gmail.com',
  url = 'https://github.com/piyushc79/RedisClusterCache/dj_rcc/', 
  download_url = 'https://github.com/piyushc79/RedisClusterCache/dj_rcc/',
  install_requires=[
      'redis>=2.10.2',
      'redis-py-cluster==1.0.0',
  ],
  keywords=[
      'redis',
      'redis cluster',
  ],
  classifiers=(
        # As from https://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Environment :: Web Environment',
        'Operating System :: POSIX',
    ) 
)
