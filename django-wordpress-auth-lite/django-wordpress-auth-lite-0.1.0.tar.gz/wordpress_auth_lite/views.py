from django.http import HttpResponse

from wordpress_auth_lite.decorators import wordpress_login_required

@wordpress_login_required
def show_session(request):
    return HttpResponse(request.wordpress_user.login)
