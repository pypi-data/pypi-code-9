from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect, render, get_object_or_404

from django.utils.lru_cache import lru_cache

from .models import AbstractGlobalSettingsCollection
from django.contrib.contenttypes.models import ContentType
from wagtail.wagtailadmin.edit_handlers import extract_panel_definitions_from_model_class,\
    ObjectList, get_form_for_model
from django.contrib import messages
from django.http.response import Http404

@lru_cache({}, 1)
def get_global_settings_edit_handler(model):
    panels = extract_panel_definitions_from_model_class(model, exclude=[])
    EditHandler = ObjectList(panels).bind_to_model(model)
    return EditHandler


@lru_cache({}, 2)
def get_global_settings_form(model, EditHandler):
    return get_form_for_model(
        model,
        formsets=EditHandler.required_formsets(),
        widgets=EditHandler.widget_overrides(),
        exclude=[])

@permission_required('wagtailadmin.access_admin')  # further permissions are enforced within the view
def choose(request):
    global_settings_list = AbstractGlobalSettingsCollection.get_global_settings_models()
    if len(global_settings_list) == 1:
        return redirect('wagtail_global_settings_edit', pk=global_settings_list[0].get_content_type().pk)

    return render(request, 'wagtail_global_settings/choose.html', {
        'has_global_settings': len(global_settings_list) != 0,
        'global_settings_list': ((global_settings.get_content_type(), global_settings._meta.verbose_name)
                           for global_settings in global_settings_list)
    })


@permission_required('wagtailadmin.access_admin')  # further permissions are enforced within the view
def edit(request, pk):
    content_type = get_object_or_404(ContentType, pk=pk)
    model = content_type.model_class()
    if not issubclass(model, AbstractGlobalSettingsCollection):
        raise Http404
    instance = model.get_solo()
    
    EditHandler = get_global_settings_edit_handler(model)
    EditForm = get_global_settings_form(model, EditHandler)

    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            messages.success(request, _('The global settings "{0!s}" has been updated').format(instance._meta.verbose_name))
            return redirect('wagtail_global_settings_edit', pk=content_type.pk)
        else:
            messages.error(request, _('The global settings could not be updated due to validation errors'))
            edit_handler = EditHandler(instance=instance, form=form)
    else:
        form = EditForm(instance=instance)
        edit_handler = EditHandler(instance=instance, form=form)

    return render(request, 'wagtail_global_settings/edit.html', {
        'model_name': instance._meta.verbose_name,
        'content_type': content_type,
        'edit_handler': edit_handler,
    })
