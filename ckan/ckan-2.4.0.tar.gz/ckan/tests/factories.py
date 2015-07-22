'''This is a collection of factory classes for building CKAN users, datasets,
etc.

These are meant to be used by tests to create any objects that are needed for
the tests. They're written using ``factory_boy``:

http://factoryboy.readthedocs.org/en/latest/

These are not meant to be used for the actual testing, e.g. if you're writing
a test for the :py:func:`~ckan.logic.action.create.user_create` function then
call :py:func:`~ckan.tests.helpers.call_action`, don't test it via the
:py:class:`~ckan.tests.factories.User` factory below.

Usage::

 # Create a user with the factory's default attributes, and get back a
 # user dict:
 user_dict = factories.User()

 # You can create a second user the same way. For attributes that can't be
 # the same (e.g. you can't have two users with the same name) a new value
 # will be generated each time you use the factory:
 another_user_dict = factories.User()

 # Create a user and specify your own user name and email (this works
 # with any params that CKAN's user_create() accepts):
 custom_user_dict = factories.User(name='bob', email='bob@bob.com')

 # Get a user dict containing the attributes (name, email, password, etc.)
 # that the factory would use to create a user, but without actually
 # creating the user in CKAN:
 user_attributes_dict = factories.User.attributes()

 # If you later want to create a user using these attributes, just pass them
 # to the factory:
 user = factories.User(**user_attributes_dict)

'''
import random
import string
import factory
import mock

import ckan.model
import ckan.logic
import ckan.tests.helpers as helpers


def _get_action_user_name(kwargs):
    '''Return the name of the user in kwargs, defaulting to the site user

    It can be overriden by explictly setting {'user': None} in the keyword
    arguments. In that case, this method will return None.
    '''

    if 'user' in kwargs:
        user = kwargs['user']
    else:
        user = helpers.call_action('get_site_user')

    if user is None:
        user_name = None
    else:
        user_name = user['name']

    return user_name


def _generate_email(user):
    '''Return an email address for the given User factory stub object.'''

    return '{0}@ckan.org'.format(user.name).lower()


def _generate_reset_key(user):
    '''Return a reset key for the given User factory stub object.'''

    return '{0}_reset_key'.format(user.name).lower()


def _generate_user_id(user):
    '''Return a user id for the given User factory stub object.'''

    return '{0}_user_id'.format(user.name).lower()


def _generate_group_title(group):
    '''Return a title for the given Group factory stub object.'''

    return group.name.replace('_', ' ').title()


def _generate_random_string(length=6):
    '''Return a random string of the defined length.'''

    return ''.join(random.sample(string.ascii_lowercase, length))


class User(factory.Factory):
    '''A factory class for creating CKAN users.'''

    # This is the class that UserFactory will create and return instances
    # of.
    FACTORY_FOR = ckan.model.User

    # These are the default params that will be used to create new users.
    fullname = 'Mr. Test User'
    password = 'pass'
    about = 'Just another test user.'

    # Generate a different user name param for each user that gets created.
    name = factory.Sequence(lambda n: 'test_user_{n}'.format(n=n))

    # Compute the email param for each user based on the values of the other
    # params above.
    email = factory.LazyAttribute(_generate_email)

    # I'm not sure how to support factory_boy's .build() feature in CKAN,
    # so I've disabled it here.
    @classmethod
    def _build(cls, target_class, *args, **kwargs):
        raise NotImplementedError(".build() isn't supported in CKAN")

    # To make factory_boy work with CKAN we override _create() and make it call
    # a CKAN action function.
    # We might also be able to do this by using factory_boy's direct SQLAlchemy
    # support: http://factoryboy.readthedocs.org/en/latest/orms.html#sqlalchemy
    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        if args:
            assert False, "Positional args aren't supported, use keyword args."
        user_dict = helpers.call_action('user_create', **kwargs)
        return user_dict


class Resource(factory.Factory):
    '''A factory class for creating CKAN resources.'''

    FACTORY_FOR = ckan.model.Resource

    name = factory.Sequence(lambda n: 'test_resource_{n}'.format(n=n))
    description = 'Just another test resource.'
    format = 'res_format'
    url = 'http://link.to.some.data'
    package_id = factory.LazyAttribute(lambda _: Dataset()['id'])

    @classmethod
    def _build(cls, target_class, *args, **kwargs):
        raise NotImplementedError(".build() isn't supported in CKAN")

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        if args:
            assert False, "Positional args aren't supported, use keyword args."

        context = {'user': _get_action_user_name(kwargs)}

        resource_dict = helpers.call_action('resource_create', context=context,
                                            **kwargs)
        return resource_dict


class ResourceView(factory.Factory):
    '''A factory class for creating CKAN resource views.

    Note: if you use this factory, you need to load the `image_view` plugin
    on your test class (and unload it later), otherwise you will get an error.

    Example::

        class TestSomethingWithResourceViews(object):
            @classmethod
            def setup_class(cls):
                if not p.plugin_loaded('image_view'):
                    p.load('image_view')

            @classmethod
            def teardown_class(cls):
                p.unload('image_view')

    '''

    FACTORY_FOR = ckan.model.ResourceView

    title = factory.Sequence(lambda n: 'test_resource_view_{n}'.format(n=n))
    description = 'Just another test resource view.'
    view_type = 'image_view'
    resource_id = factory.LazyAttribute(lambda _: Resource()['id'])

    @classmethod
    def _build(cls, target_class, *args, **kwargs):
        raise NotImplementedError(".build() isn't supported in CKAN")

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        if args:
            assert False, "Positional args aren't supported, use keyword args."

        context = {'user': _get_action_user_name(kwargs)}

        resource_dict = helpers.call_action('resource_view_create',
                                            context=context, **kwargs)
        return resource_dict


class Sysadmin(factory.Factory):
    '''A factory class for creating sysadmin users.'''

    FACTORY_FOR = ckan.model.User

    fullname = 'Mr. Test Sysadmin'
    password = 'pass'
    about = 'Just another test sysadmin.'

    name = factory.Sequence(lambda n: 'test_sysadmin_{n}'.format(n=n))

    email = factory.LazyAttribute(_generate_email)
    sysadmin = True

    @classmethod
    def _build(cls, target_class, *args, **kwargs):
        raise NotImplementedError(".build() isn't supported in CKAN")

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        if args:
            assert False, "Positional args aren't supported, use keyword args."

        user = target_class(**dict(kwargs, sysadmin=True))
        ckan.model.Session.add(user)
        ckan.model.Session.commit()
        ckan.model.Session.remove()

        # We want to return a user dict not a model object, so call user_show
        # to get one. We pass the user's name in the context because we want
        # the API key and other sensitive data to be returned in the user
        # dict.
        user_dict = helpers.call_action('user_show', id=user.id,
                                        context={'user': user.name})
        return user_dict


class Group(factory.Factory):
    '''A factory class for creating CKAN groups.'''

    FACTORY_FOR = ckan.model.Group

    name = factory.Sequence(lambda n: 'test_group_{n}'.format(n=n))
    title = factory.LazyAttribute(_generate_group_title)
    description = 'A test description for this test group.'

    user = factory.LazyAttribute(lambda _:
                                 helpers.call_action('get_site_user'))

    @classmethod
    def _build(cls, target_class, *args, **kwargs):
        raise NotImplementedError(".build() isn't supported in CKAN")

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        if args:
            assert False, "Positional args aren't supported, use keyword args."

        context = {'user': _get_action_user_name(kwargs)}

        group_dict = helpers.call_action('group_create',
                                         context=context,
                                         **kwargs)
        return group_dict


class Organization(factory.Factory):
    '''A factory class for creating CKAN organizations.'''

    # This is the class that OrganizationFactory will create and return
    # instances of.
    FACTORY_FOR = ckan.model.Group

    # These are the default params that will be used to create new
    # organizations.
    type = 'organization'
    is_organization = True

    title = 'Test Organization'
    description = 'Just another test organization.'
    image_url = 'http://placekitten.com/g/200/100'

    # Generate a different group name param for each user that gets created.
    name = factory.Sequence(lambda n: 'test_org_{n}'.format(n=n))

    @classmethod
    def _build(cls, target_class, *args, **kwargs):
        raise NotImplementedError(".build() isn't supported in CKAN")

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        if args:
            assert False, "Positional args aren't supported, use keyword args."

        context = {'user': _get_action_user_name(kwargs)}

        group_dict = helpers.call_action('organization_create',
                                         context=context,
                                         **kwargs)
        return group_dict


class Related(factory.Factory):
    '''A factory class for creating related items.'''

    FACTORY_FOR = ckan.model.Related

    type = 'idea'
    description = 'Look, a description!'
    url = 'http://example.com'

    title = factory.Sequence(lambda n: 'test title {n}'.format(n=n))

    @classmethod
    def _build(cls, target_class, *args, **kwargs):
        raise NotImplementedError(".build() isn't supported in CKAN")

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        if args:
            assert False, "Positional args aren't supported, use keyword args."

        context = {'user': _get_action_user_name(kwargs)}
        related_dict = helpers.call_action('related_create', context=context,
                                           **kwargs)
        return related_dict


class Dataset(factory.Factory):
    '''A factory class for creating CKAN datasets.'''

    FACTORY_FOR = ckan.model.Package

    # These are the default params that will be used to create new groups.
    title = 'Test Dataset'
    description = 'Just another test dataset.'

    # Generate a different group name param for each user that gets created.
    name = factory.Sequence(lambda n: 'test_dataset_{n}'.format(n=n))

    @classmethod
    def _build(cls, target_class, *args, **kwargs):
        raise NotImplementedError(".build() isn't supported in CKAN")

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        if args:
            assert False, "Positional args aren't supported, use keyword args."

        context = {'user': _get_action_user_name(kwargs)}

        dataset_dict = helpers.call_action('package_create',
                                           context=context,
                                           **kwargs)
        return dataset_dict


class MockUser(factory.Factory):
    '''A factory class for creating mock CKAN users using the mock library.'''

    FACTORY_FOR = mock.MagicMock

    fullname = 'Mr. Mock User'
    password = 'pass'
    about = 'Just another mock user.'
    name = factory.Sequence(lambda n: 'mock_user_{n}'.format(n=n))
    email = factory.LazyAttribute(_generate_email)
    reset_key = factory.LazyAttribute(_generate_reset_key)
    id = factory.LazyAttribute(_generate_user_id)

    @classmethod
    def _build(cls, target_class, *args, **kwargs):
        raise NotImplementedError(".build() isn't supported in CKAN")

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        if args:
            assert False, "Positional args aren't supported, use keyword args."
        mock_user = mock.MagicMock()
        for name, value in kwargs.items():
            setattr(mock_user, name, value)
        return mock_user


class SystemInfo(factory.Factory):
    '''A factory class for creating SystemInfo objects (config objects
       stored in the DB).'''

    FACTORY_FOR = ckan.model.SystemInfo

    key = factory.Sequence(lambda n: 'test_config_{n}'.format(n=n))
    value = _generate_random_string()

    @classmethod
    def _build(cls, target_class, *args, **kwargs):
        raise NotImplementedError(".build() isn't supported in CKAN")

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        if args:
            assert False, "Positional args aren't supported, use keyword args."

        ckan.model.system_info.set_system_info(kwargs['key'],
                                               kwargs['value'])
        obj = ckan.model.Session.query(ckan.model.system_info.SystemInfo) \
                                .filter_by(key=kwargs['key']).first()

        return obj


def validator_data_dict():
    '''Return a data dict with some arbitrary data in it, suitable to be passed
    to validator functions for testing.

    '''
    return {('other key',): 'other value'}


def validator_errors_dict():
    '''Return an errors dict with some arbitrary errors in it, suitable to be
    passed to validator functions for testing.

    '''
    return {('other key',): ['other error']}


class Vocabulary(factory.Factory):
    '''A factory class for creating tag vocabularies.'''

    FACTORY_FOR = ckan.model.Vocabulary
    name = factory.Sequence(lambda n: 'test_vocabulary_{n}'.format(n=n))

    @classmethod
    def _build(cls, target_class, *args, **kwargs):
        raise NotImplementedError(".build() isn't supported in CKAN")

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        if args:
            assert False, "Positional args aren't supported, use keyword args."
        return helpers.call_action('vocabulary_create', **kwargs)
