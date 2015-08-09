from distutils.core import setup
setup(name='PyNimFFI',
      version='0.1',
      description='Call nim functions from Python.',
      author='Peter Row',
      author_email='peter.row@gmail.com',
      url='https://gitlab.com/peter-row/pyNimFFI/tree/master',
      py_modules=['PyNimFFI'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT',
          'Programming Language :: Python :: 2',
          ],
      requires=[
        "cffi",
        ],
        long_description="""
A wrapper to allow nim functions to be called in Python.

It requires a nim package (also called PyNimFFI) to be installed, through nimble.

It uses cffi, and has some performance overhead, but has a reasonable number of features.

Ints, cstrings, and floats can be sent natively.

Exceptions are wrapped, and propagated back to Python.

Opaque types can be wrapped as subclasses of a "NimBase" class, and have a delete method created (which decrements the nim ref count - allowing garbage collection to happen correctly).

Note, there is apparently another nim / python bridge in the works, and may turn out to be better."""
)
