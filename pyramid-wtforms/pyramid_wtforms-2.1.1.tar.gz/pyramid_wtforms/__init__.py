from . import validators
from .fields import *
from .forms import SecureForm
from wtforms import widgets
from wtforms.form import Form
from wtforms.validators import ValidationError
import pkg_resources

__version__ = pkg_resources.get_distribution('pyramid_wtforms').version
