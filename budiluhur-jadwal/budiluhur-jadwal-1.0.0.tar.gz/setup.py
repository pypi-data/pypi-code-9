from setuptools import setup

long_description = '''
`Application Programming Interface` untuk mengambil data Jadwal
harian perkuliahan dari semua fakultas di Kampus `Universitas Budiluhur Jakarta`.

## Quick Start

```python
from budiluhur.jadwal import fakultas

# inisialisasi class Fakultas
f = fakultas.Fakultas()
fakultas_bl = f.get_all()
print(fakultas_bl)
```
'''

setup(
	name             = 'budiluhur-jadwal',
	version          = '1.0.0',
	description      = 'Python API Jadwal Perkulahan Budiluhur',
	author           = 'Yanwar Solahudin',
	author_email     = 'yanwarsolahudinn@gmail.com',
	url              = 'https://github.com/yanwarsolahudinn/budiluhur-jadwal',
	download_url     = 'https://github.com/yanwarsolahudinn/budiluhur-jadwal/archive/master.zip',
	include_package_data = True,
	long_description = long_description,
	keywords         = ['API', 'JSON', 'budiluhur', 'jadwal', 'track', 'schedule', 'kuliah'],
	classifiers      = [],
	install_requires = ["requests", "beautifulsoup4", "python-Levenshtein", "rft1d"]
)
