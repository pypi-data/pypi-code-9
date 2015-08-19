from zope.interface import Interface


class IScaffoldingRecipe(Interface):
    """ Take the logic to build scaffolding
        elements, like extjs store, model..
    """

    def __init__(self, context, description, request):
        pass

    def __call__(self):
        pass


class IScaffoldingRecipeModel(IScaffoldingRecipe):
    pass


class IScaffoldingRecipeStore(IScaffoldingRecipe):
    pass


class IScaffoldingRecipeBufferedStore(IScaffoldingRecipe):
    pass


class IScaffoldingRecipeForm(IScaffoldingRecipe):
    pass


class IScaffoldingRecipeDisplay(IScaffoldingRecipe):
    pass


class IScaffoldingRecipeGrid(IScaffoldingRecipe):
    pass


class IScaffoldingRecipeEditGrid(IScaffoldingRecipe):
    pass


class IRecipeDescriptive(Interface):
    """ Define a description for each recipe.
    """


class IFieldBuilder(Interface):
    """
    """

    def __init__(self, recipe, field):
        pass

    def __call__(self):
        pass


class IFormFields(Interface):
    """A colection of form fields (IFormField objects)
    """

    def __len__():
        """Get the number of fields
        """

    def __iter__():
        """Iterate over the form fields
        """

    def __getitem__(name):
        """Return the form field with the given name

        If the desired firld has a prefix, then the given name should
        be the prefix, a dot, and the unprefixed name.  Otherwise, the
        given name is just the field name.

        Raise a KeyError if a field can't be found for the given name.
        """

    def get(name, default=None):
        """Return the form field with the given name

        If the desired firld has a prefix, then the given name should
        be the prefix, a dot, and the unprefixed name.  Otherwise, the
        given name is just the field name.

        Return the default if a field can't be found for the given name.
        """

    def __add__(form_fields):
        """Add two form fields collections (IFormFields)

        Return a new IFormFields that is the concatination of the two
        IFormFields.
        """

    def select(*names):
        """Select fields with given names in order

        Return a new IFormFields that is a selection from the original
        IFormFields that has the named fields in the specified order.
        """

    def omit(*names):
        """Omit fields with given names
        """
