from setuptools import setup

long_description = '''

API Sistem Pengecekan Jadwal Kuliah Universitas Budiluhur
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. topic:: Simple API Jadwal Budiluhur

       Application Programming Interface
       untuk mengambil data Jadwal
       harian perkuliahan dari semua
       fakultas di Kampus `Universitas Budiluhur Jakarta`.

**Quick Start**

.. code:: python

    from budiluhur.jadwal import fakultas
    # inisialisasi class Fakultas
    f = fakultas.Fakultas()
    fakultas_bl = f.get_all()
    print(fakultas_bl)

**Instalasi**

.. code::

    $ pip install budiluhur-jadwal

**Fakultas Class**

.. code:: python

    from budiluhur.jadwal import fakultas

    # inisialisasi class Fakultas
    f = fakultas.Fakultas()

**dapatkan semua fakultas**


.. code:: python

    from budiluhur.jadwal import fakultas

    # inisialisasi class Fakultas
    f = fakultas.Fakultas()
    fakultas_bl = f.get_all()
    print(fakultas_bl)

**Full Dokumentasi**

`Dokumentasi API Sistem Cek Jadwal Kehadiran Dosen <https://github.com/yanwarsolahudinn/budiluhur-jadwal>`_

'''

CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Natural Language :: Indonesian",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

setup(
	name             = 'budiluhur-jadwal',
	version          = '1.1.0',
	description      = 'Python API Jadwal Perkulahan Budiluhur',
	author           = 'Yanwar Solahudin',
	author_email     = 'yanwarsolahudinn@gmail.com',
	url              = 'https://github.com/yanwarsolahudinn/budiluhur-jadwal',
	download_url     = 'https://github.com/yanwarsolahudinn/budiluhur-jadwal/archive/master.zip',
	include_package_data = True,
	long_description = long_description,
	keywords         = ['API', 'JSON', 'budiluhur', 'jadwal', 'track', 'schedule', 'kuliah'],
	classifiers      = CLASSIFIERS,
	install_requires = ["requests", "beautifulsoup4", "python-Levenshtein", "rft1d"]
)
