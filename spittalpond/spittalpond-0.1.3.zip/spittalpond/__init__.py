"""
Spittalpond Oasis API Package
=============================

Spittalpond is a Python interface for the OasisLMF Django API webservices. It acts as a front-end that
allows you to run models, exposures and other useful webservices in Oasis. Effectively, it's turns
you Oasis style .csv files into useful GUL data!

Basic usage of spittalpond package:

    >>> import spittalpond
    >>> spit = spittalpond.SpittalPond("http://127.0.0.1:8000", "root")
    >>> spit.model.do_login("password")
    You are logged into Mid-tier
    >>> resp = spit.model.do_request("http://127.0.0.1:8000/oasis/listGUL/")
    >>> resp.content
    '[{"optionValue":1,"canWrite":true,"optionDisplay":"GUL","success":true,"canRead":true},{"optionValue":2,"canWrite":true
    ,"optionDisplay":"spittalGUL","success":true,"canRead":true}]'
    >>>


Full documentation is at <http://beckettsimmons.github.io/spittalpond/docs/>.
"""
from .spittalpond import SpittalPond
