from fanstatic import Library, Resource, Group

library = Library('mocha', 'resources')

# Define the resources in the library like this.
# For options and examples, see the fanstatic documentation.
mocha = Group([
    Resource(library, 'mocha.js'),
    Resource(library, 'mocha.css')
    ])
