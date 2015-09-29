import os


def get_includes():
    import c_array_defs
    r"""
    Return the directory that contains the `c_array_defs` Cython *.hpp and
    *.pxd header files.

    Extension modules that need to compile against `c_array_defs` should use
    this function to locate the appropriate include directory.

    Notes
    -----
    When using ``distutils``, for example in ``setup.py``.
    ::

        import c_array_defs
        ...
        Extension('extension_name', ...
                  include_dirs=[...] + c_array_defs.get_includes())
        ...

    """
    return [os.path.join(os.path.dirname(c_array_defs.__file__), 'Arduino', 'CArrayDefs')]
