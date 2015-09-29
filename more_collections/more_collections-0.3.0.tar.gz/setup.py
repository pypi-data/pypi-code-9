from distutils.core import setup

setup(
    name="more_collections",
    packages = ['more_collections'],
    version="0.3.0",
    author="Mario Wenzel",
    author_email="maweki@gmail.com",
    url="https://github.com/maweki/more-collections",
    description="more_collections is a Python library providing more collections (multisets, orderable multisets, hashable dictionaries, ...).",
    license="MIT",
    classifiers=[
"Programming Language :: Python :: 2.7",
"Programming Language :: Python :: 3",
"Programming Language :: Python :: 3.2",
"Programming Language :: Python :: 3.3",
"Programming Language :: Python :: 3.4",
"Programming Language :: Python :: 3.5",
"Operating System :: OS Independent",
"Development Status :: 5 - Production/Stable",
"Intended Audience :: Developers",
"Intended Audience :: Science/Research",
"Intended Audience :: Education",
"License :: OSI Approved :: MIT License",
"Topic :: Software Development :: Libraries :: Python Modules"
],
keywords='collections multiset frozendict development',
    long_description=
"""
This package provides some more collections than the standard collections package.

The package currently provides:

- **puredict**/**frozendict** - a functionally **pure** and **immutable dictionary** that is even **hashable**,
if all keys and values are hashable.
- **multiset**/**frozenmultiset** - a multiset implementation
- **orderable_multiset**/**orderable_frozenmultiset** - a multiset implementation for orderable carriers so that
multisets of those elements themselves are orderable, even including **nestable_orderable_frozenmultiset**
which is a multiset-ordering-extension that gives a total ordering for arbitrarily nested multisets over an orderable carrier.

If you want to see any more collections, contact me, open a ticket (I'll happily implement it) or send in a patch.

See https://github.com/maweki/more-collections for a full guide and more information.
"""
)
