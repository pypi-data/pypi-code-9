from distutils.core import setup
from distutils.extension import Extension
from glob import glob

try:
    from Cython.Build import cythonize
    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False

if USE_CYTHON:
    src_ext = 'pyx'
else:
    src_ext = 'c'

sources = ['src/cmarkpy.{}'.format(src_ext)]
sources.extend(glob('src/cmark/*.c'))

extensions = [
    Extension(
        'cmarkpy',
        sources,
        include_dirs=['src/cmark'],
        define_macros=[('CMARK_STATIC_DEFINE', None)],
        extra_compile_args=['-std=c99'],
    )
]

if USE_CYTHON:
    extensions = cythonize(extensions)

setup(
    name='cmarkpy',
    version='0.1.3',
    ext_modules=extensions,
    author='Daniel Trojanowski',
    author_email='daniel.trojanowski@gmail.com',
    description='CommonMark (libcmark) bindings for Python',
    license='BSD',
)
