#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Welcome to docfly documentation
================================================================================

**docfly is a pure python package to help you build fancy searchable, auto-generated API reference document.**

QuickLink:

- `Home page <https://github.com/MacHu-GWU/docfly-project>`_
- `PyPI download <https://pypi.python.org/pypi/docfly>`_
- `English document <https://pypi.python.org/pypi/docfly>`_
- `Chinese document <https://github.com/MacHu-GWU/docfly-project>`_
- `Install <install_>`_

Notice, everything below here is tested in Windows, and mostly also works for Linux, Unix and Mac.


Introduction
--------------------------------------------------------------------------------

I assume you already know how to use `sphinx <http://sphinx-doc.org/>`_ to build your own document site. After you run: ``$ sphinx-quickstart``, you may see this in the ``index.rst`` file::

    Indices and tables
    ==================

    * :ref:`genindex`
    * :ref:`modindex`
    * :ref:`search`

This piece is for built-in automate tools ``sphinx.ext.autodoc`` to generate doc from your docstring. 

Let's take a look at one of the most successful open source Python project ``requests``. This is how's the API document looks like:
`requests API reference <http://docs.python-requests.org/en/stable/api/>`_. And this is `the code <https://raw.githubusercontent.com/kennethreitz/requests/master/docs/api.rst>`_ behind that page.

God, even though you can use ``..autoclass::``, ``..autofunction::`` to generate docs, but you still need to type it in the ``api.rst`` file manually. **Is there any way we can make it easier and EVEN BETTER?**, YES, that is what **docfly** for.

Now let's see an example project built with docfly: http://sqlite4dummy-project.readthedocs.org/py-modindex.html

See that tree structure of the modules and subpackages? If you click on a package, then it jump to a page with the docstring in ``package.__init__.py`` and link for its sub-subpackage and modules.

And everything you need, is to run `a little python script <https://github.com/MacHu-GWU/sqlite4dummy-project/blob/master/create_doctree.py>`_ with docfly:

.. code-block:: python

    from docfly import Docfly

    docfly = Docfly("sqlite4dummy", dst="source") # define the package name, make sure it's importable
    docfly.fly()

BOOM! Now you got not only the nicely structured API reference document, but also the ability to link any module, package, function, class, method's doc anywhere you want. Just use the `python domain markup <http://sphinx-doc.org/domains.html#the-python-domain>`_, like: ``:class:`<package.module.class>```.


The explain
--------------------------------------------------------------------------------

OK, OK, I gonna reveal the magic behind this now.

.. code-block:: python

    from docfly import Docfly

    docfly = Docfly(package_name="sqlite4dummy", dst="source", ignore=[])

Docfly class has three initiation parameters:

1. ``package_name`` defines your package, which is importable and installed under ``site-packages`` directory.
2. ``dst`` is the place that ``docfly`` will create a tree ``.rst`` file structure exactly the same as your package. So in this example, it creates ``source\sqlite4dummy...``. And in each ``.rst`` file, the content cites all members for each module by default.
3. ``ignore`` defines the subpackage and module you want to ignore. The syntax is similar to Github ``.gitignore`` file. For example: ``["sqlite4dummy.tests", "sqlite4dummy.zzz_manual_install.py"]`` will prevent creating doc for subpackage ``sqlite4dummy.tests`` and module ``sqlite4dummy.zzz_manual_install.py``.

So basically what you do is to set your destination (dst) to the directory of your sphinx ``conf.py`` file.

**docfly makes doc fly.**


More example
--------------------------------------------------------------------------------

You can download the source code at https://github.com/MacHu-GWU/docfly-project/archive/master.zip. There's an example project ``toppackage``, you can try build a easy doc sites for ``toppackage``. You can follow these steps:

1. Install example package ``toppackage``::

        $ cd docfly-project\toppackage-project
        $ python setup.py build
        $ python setup.py install

2. Then install ``docfly``::

        $ pip install docfly
        or
        $ cd docfly-project
        $ python setup.py build
        $ python setup.py install

3. Then run ``create_doctree.py``::

        $ cd docfly-project\toppackage-project
        $ python create_doctree.py

4. Then build the doc site::

        $ cd docfly-project\toppackage-project
        $ make html

5. Then go enjoy your doc site::

        $ cd docfly-project\toppackage-project\build\html
        $ index.html


.. _install:

Install
--------------------------------------------------------------------------------

``docfly`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install docfly

To upgrade to latest version:

.. code-block:: console
    
    $ pip install --upgrade docfly
"""

from .fly import Docfly

__version__ = "0.0.1"