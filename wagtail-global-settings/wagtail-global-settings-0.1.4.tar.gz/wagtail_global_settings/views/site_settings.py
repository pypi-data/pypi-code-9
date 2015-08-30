from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.shortcuts import redirect, render, get_object_or_404
from wagtail_global_settings.models import AbstractSiteSettingsCollection
from wagtail.wagtailcore.models import Site
from django.contrib.contenttypes.models import ContentType
from django.http.response import Http404
from django.utils.lru_cache import lru_cache
from wagtail.wagtailadmin.edit_handlers import extract_panel_definitions_from_model_class,\
    ObjectList, get_form_for_model
from django.contrib import messages
from wagtail_global_settings.permissions import user_can_edit_site_settings,\
    user_can_edit_global_settings_type
from django.core.urlresolvers import reverse_lazy, reverse

@lru_cache({}, 1)
def get_site_settings_edit_handler(model):
    panels = extract_panel_definitions_from_model_class(model, exclude=['site'])
    EditHandler = ObjectList(panels).bind_to_model(model)
    return EditHandler


@lru_cache({}, 2)
def get_site_settings_form(model, EditHandler):
    return get_form_for_model(
        model,
        formsets=EditHandler.required_formsets(),
        widgets=EditHandler.widget_overrides(),
        exclude=['site'])

@permission_required('wagtailadmin.access_admin', login_url=reverse_lazy('wagtailadmin_login'))
@user_passes_test(user_can_edit_site_settings, login_url=reverse_lazy('wagtailadmin_login'))
def choose_site(request):
    site_settings_list = AbstractSiteSettingsCollection.get_global_settings_models()
    if len(site_settings_list) == 0:
        return render(request, 'wagtail_global_settings/choose_site.html', {
            'has_global_settings': False,
            'global_settings_list': []
        })
    sites = Site.objects.all()
    
    if sites.count() == 1:
        return redirect('wagtail_site_settings_choose', pk=sites.first().pk)

    return render(request, 'wagtail_global_settings/choose_site.html', {
        'has_site_settings': sites.count() != 0,
        'sites_list': sites,
    })

@permission_required('wagtailadmin.access_admin', login_url=reverse_lazy('wagtailadmin_login'))
@user_passes_test(user_can_edit_site_settings, login_url=reverse_lazy('wagtailadmin_login'))
def choose(request, pk):
    site = get_object_or_404(Site, pk=pk)
    site_settings_list = AbstractSiteSettingsCollection.get_global_settings_models()
    if len(site_settings_list) == 1:
        return redirect('wagtail_site_settings_edit', pk=site.pk, ct_pk=site_settings_list[0].get_content_type().pk)

    return render(request, 'wagtail_global_settings/choose_site_setting.html', {
        'site': site,
        'has_global_settings': len(site_settings_list) != 0,
        'site_settings_list': ((global_settings.get_content_type(), global_settings._meta.verbose_name)
                           for global_settings in site_settings_list)
    })

@permission_required('wagtailadmin.access_admin', login_url=reverse_lazy('wagtailadmin_login'))
@user_passes_test(user_can_edit_site_settings, login_url=reverse_lazy('wagtailadmin_login'))
def edit(request, pk, ct_pk):
    content_type = get_object_or_404(ContentType, pk=ct_pk)
    if not user_can_edit_global_settings_type(request.user, content_type):
        return redirect(reverse('wagtailadmin_login'))
    site = get_object_or_404(Site, pk=pk)
    model = content_type.model_class()
    if not issubclass(model, AbstractSiteSettingsCollection):
        raise Http404
    instance = model.objects.for_site(site)
    
    EditHandler = get_site_settings_edit_handler(model)
    EditForm = get_site_settings_form(model, EditHandler)

    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            messages.success(request, _('The site settings "{0!s}" has been updated').format(instance._meta.verbose_name))
            return redirect('wagtail_site_settings_choose', pk=site.pk)
        else:
            messages.error(request, _('The global settings could not be updated due to validation errors'))
            edit_handler = EditHandler(instance=instance, form=form)
    else:
        form = EditForm(instance=instance)
        edit_handler = EditHandler(instance=instance, form=form)

    return render(request, 'wagtail_global_settings/edit_site_setting.html', {
        'site': site,
        'model_name': instance._meta.verbose_name,
        'content_type': content_type,
        'edit_handler': edit_handler,
    })
