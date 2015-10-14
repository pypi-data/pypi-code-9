"""
This implements a simple profile in one file.
"""
from django.contrib import messages
from django.template import RequestContext
from django.shortcuts import render_to_response

from changer.c5.simpleprofile import SIMPLEPROFILE_PROFILE_UPDATED
from changer.c5.simpleprofile.forms import ProfileForm
from changer.c5.simpleprofile.models import Profile


def get_or_create_profile(user):
    """
    Shortcut method
    """
    from django.contrib.auth.models import SiteProfileNotAvailable
    try:
        profile = user.get_profile()
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)
    except (SiteProfileNotAvailable), e:
        raise e
    return profile


def view_profile(request):
    """
    Simple profile view to update/view your profile.
    """
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            user = request.user
            user.email = request.POST['email']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            profile = user.get_profile()
            profile.telephone = request.POST['telephone']
            user.save()
            profile.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 SIMPLEPROFILE_PROFILE_UPDATED)
    else:
        profile = get_or_create_profile(request.user)
        fields = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'telephone': getattr(profile, 'telephone', ''),
        }
        profile_form = ProfileForm(initial=fields)
    return render_to_response('profile.html',
                              {'form': profile_form},
                              RequestContext(request))
