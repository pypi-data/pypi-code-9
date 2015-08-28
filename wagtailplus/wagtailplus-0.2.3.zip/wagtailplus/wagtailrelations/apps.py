"""
Contains application configuration.
"""
from django.contrib.admin.apps import SimpleAdminConfig
from django.utils.functional import cached_property


class WagtailRelationsAppConfig(SimpleAdminConfig):
    name                = 'wagtailplus.wagtailrelations'
    label               = 'wagtailrelations'
    verbose_name        = 'Relations'

    @cached_property
    def applicable_models(self):
        """
        Returns a list of model classes that subclass Page
        and include a "tags" field.

        :rtype: list.
        """
        from django.apps import apps
        from wagtail.wagtailcore.models import Page

        applicable = []

        for model in apps.get_models():
            meta    = getattr(model, '_meta')
            fields  = meta.get_all_field_names()

            if issubclass(model, Page) and 'tags' in fields:
                applicable.append(model)

        return applicable

    def add_relationship_edit_handlers(self):
        """
        Add edit handler that includes "related" panels to applicable
        model classes that don't explicitly define their own edit handler.
        """
        from wagtail.wagtailadmin.views.pages import PAGE_EDIT_HANDLERS

        for model in self.applicable_models:
            if model not in PAGE_EDIT_HANDLERS:
                if hasattr(model, 'edit_handler'):
                    edit_handler = model.edit_handler
                else:
                    edit_handler = self.get_related_edit_handler(model)

                PAGE_EDIT_HANDLERS[model] = edit_handler.bind_to_model(model)

    def add_relationship_methods(self):
        """
        Adds relationship methods to applicable model classes.
        """
        from wagtailplus.wagtailrelations.models import Entry

        @cached_property
        def related(instance):
            return instance.get_related()

        @cached_property
        def related_with_scores(instance):
            return instance.get_related_with_scores()

        def get_related(instance):
            entry = Entry.objects.get_for_model(instance)[0]
            return entry.get_related()

        def get_related_with_scores(instance):
            entry = Entry.objects.get_for_model(instance)[0]
            return entry.get_related_with_scores()

        for model in self.applicable_models:
            model.add_to_class(
                'get_related',
                get_related
            )
            model.add_to_class(
                'get_related_with_scores',
                get_related_with_scores
            )
            model.add_to_class(
                'related',
                related
            )
            model.add_to_class(
                'related_with_scores',
                related_with_scores
            )

    @staticmethod
    def get_related_edit_handler(model):
        """
        Returns an edit handler instance with related panels for
        specified model class.

        :param model: the model class.
        :rtype: wagtail.wagtailadmin.edit_handlers.TabbedInterface.
        """
        from django.utils.translation import ugettext_lazy as _

        from wagtail.wagtailadmin.edit_handlers import (
            ObjectList,
            TabbedInterface
        )

        from wagtailplus.wagtailrelations.edit_handlers import RelatedPanel

        tabs = []

        if model.content_panels:
            tabs.append(ObjectList(
                model.content_panels,
                heading = _(u'Content')
        ))
        if model.promote_panels:
            tabs.append(ObjectList(
                model.promote_panels,
                heading = _(u'Promote')
            ))
        if model.settings_panels:
            tabs.append(ObjectList(
                model.settings_panels,
                heading     = _(u'Settings'),
                classname   = 'settings')
            )

        tabs.append(ObjectList(
            [RelatedPanel(),],
            heading = _(u'Related')
        ))

        return TabbedInterface(tabs)

    def ready(self):
        """
        Finalizes application configuration.
        """
        #noinspection PyUnresolvedReferences
        import wagtailplus.wagtailrelations.signals.handlers

        self.add_relationship_edit_handlers()
        self.add_relationship_methods()

        super(WagtailRelationsAppConfig, self).ready()
