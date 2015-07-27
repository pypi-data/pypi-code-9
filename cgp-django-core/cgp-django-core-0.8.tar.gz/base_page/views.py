from django.conf import settings
from django.contrib.auth.views import login
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponsePermanentRedirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import DetailView
from django.views.generic.list import MultipleObjectMixin


from .decorators import admins_skip_cache, users_skip_cache
from .models import PageBase

class NonAdminCachableView(object):

    @method_decorator(admins_skip_cache)
    def dispatch(self, *args, **kwargs):
        return super(NonAdminCachableView, self).dispatch(*args, **kwargs)

class NonUserCachableView(object):

    @method_decorator(users_skip_cache)
    def dispatch(self, *args, **kwargs):
        return super(NonUserCachableView, self).dispatch(*args, **kwargs)    




class PageRedirectHandler(MultipleObjectMixin):

    list_model = None
    object = None

    def get_list_queryset(self):
        if self.list_queryset is not None:
            list_queryset = self.list_queryset
            if hasattr(list_queryset, '_clone'):
                list_queryset = list_queryset._clone()
        elif self.list_model is not None:
            list_queryset = self.list_model._default_manager.all()
        else:
            raise ImproperlyConfigured("'%s' must define 'queryset' or 'model'"
                                       % self.__class__.__name__)
        return list_queryset
   
    
    def find_media(self, request):
        """
        Override in subclass
        """
        #return get_legacy_media_url(request)     
        raise Http404(_("Legacy Media Not Implemented"))

    def find_legacy_url(self, request):
        """
        Override in subclass
        """
        #return get_legacy_url(request)     
        raise Http404(_("Legacy URL Not Implemented"))

    def get_object_list(self):
        #OVerride in subclass
        return []


    def get(self, request, *args, **kwargs):
        
        
        #Find Page
        try:

            if not self.object:
                self.object = self.get_object()

            if self.list_model:
                self.object_list = self.get_list_queryset()
            else:
                self.object_list = []



            #TODO -- switch from 'is_superuser' to user.has_perm(...)
            is_staff = self.request.user and self.request.user.is_staff

            #Check published state
            if self.object.state < PageBase.PUBLISHED:
                if self.object.state > PageBase.UNPUBLISHED:
                    if is_staff:
                        #allow staff to view WIP and Needs Review
                        pass
                    else:

                        #If page is unpublished, set redirect
                        if self.object.redirect_page == True:
                            return HttpResponsePermanentRedirect( self.object.redirect_path )

                        #print "Found item, but it is not yet published"
                        raise Http404(_("%s is not published."%(self.model._meta.verbose_name.title())))
                else:

                    #If page is unpublished, use redirect
                    if self.object.redirect_page == True:
                        return HttpResponsePermanentRedirect( self.object.redirect_path )

                    #print "Found item, but it is unpublished"
                    raise Http404(_("%s is unpublished."%(self.model._meta.verbose_name.title())))


            return super(PageRedirectHandler, self).get(request, **kwargs)


        except Http404:         


            if settings.DEBUG:
                print "URL NOT FOUND. 1 - Try Media App"
            try:
                
                return self.find_media(request)

            except Http404:             

                if settings.DEBUG:
                    print "URL NOT FOUND. 2 - Try Legacy URL App"               
                try:                    
                                      
                    return self.find_legacy_url(request)

                except Http404:
                    pass
            
            path = request.path

            #Try to redirect to slashed url:
            if not path.endswith("/"):
                if settings.DEBUG:
                    print "URL NOT FOUND. Try appending a slash"
                newpath = u"%s/"%(path)
                return HttpResponsePermanentRedirect(newpath)                

            raise Http404(_("%s not found."%(self.model._meta.verbose_name.title())))

class PagePermissionsView(DetailView):
    template_name = "templates/default.html"

    def get_queryset(self):
        """
        Returns the pages that can be seen by the user. Staff member
        can preview on site unpublished pages.
        """
        queryset = super(PagePermissionsView, self).get_queryset()
        is_staff = self.request.user and self.request.user.is_staff
        if not is_staff:
            queryset = queryset.filter(state=PageBase.PUBLISHED)
        return queryset

    def get_object(self, queryset=None):
        """
        Returns the Page for located at the `path` or 404
        """
        # We need to start by a /z

        if self.object:
            return self.object

        if self.kwargs.get('path'):
            path = "/" + self.kwargs.get('path', '')
        else:
            path = self.request.path
        queryset = self.get_queryset()

        try:
            obj = queryset.filter(Q(path=path)|Q(path_override=path))[0]


        except:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                    {'verbose_name': queryset.model._meta.verbose_name})

        return obj

    def render_to_response(self, context, **response_kwargs):
        
        #If page has special authentication:
        if self.object.authentication_required > 0:            
            if self.object.authentication_required >= PageBase.REGISTERED_USER and not self.request.user.is_authenticated():
                return HttpResponseRedirect( reverse("auth_login") )
            elif self.object.authentication_required >= PageBase.ADMIN and self.request.user.is_staff == False:
                return HttpResponseForbidden()
        
        
        #If page is a redirect page:
        if self.object.redirect_page == True:
            return HttpResponsePermanentRedirect( self.object.redirect_path )
            
        return super(PagePermissionsView, self).render_to_response(context, **response_kwargs)

    def get_template_names(self):
        names = super(PagePermissionsView, self).get_template_names()
        if self.object and hasattr(self.object, "template_name"):
            name = getattr(self.object, "template_name")
            if name:
                names.insert(0, name)
        return names



class PageDetail(NonUserCachableView, PageRedirectHandler, PagePermissionsView):
    pass     