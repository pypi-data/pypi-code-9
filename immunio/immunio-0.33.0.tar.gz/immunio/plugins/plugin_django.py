from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from functools import (
    partial,
    wraps,
)
from hashlib import sha1
import types

from immunio.logger import log
from immunio.patcher import monkeypatch


# Set name so plugin can be enabled and disabled.
NAME = "django"


def sha1hash(value):
    """
    Return the sha1 hash of the provided value, or None if `value` is None.
    """
    if value is None:
        return None
    return sha1(value).hexdigest()


def add_hooks(run_hook, get_agent_func=None):
    """
    Add our hooks into the django library functions.
    """
    try:
        import django
        import django.conf
    except ImportError:
        return None

    # Install a hook to capture newly created wsgi apps and wrap them.
    hook_get_wsgi_application(run_hook, get_agent_func)

    # This installs all the other settings-dependent hooks as well, ensuring
    # that it does so only after settings are configured.
    hook_settings(run_hook)

    meta = {
        "version": django.get_version(),
    }

    return meta


def hook_get_wsgi_application(run_hook, get_agent_func):
    """
    Wrap the `get_wsgi_application()` function so we can wrap each WSGI
    app as it is produced. This also creates the Agent if it hasn't been
    created yet.
    """
    try:
        import django.core.wsgi
    except ImportError:
        return

    # If we don't have a `get_agent_func()` defined the app will be
    # wrapped elsewhere.
    if get_agent_func:
        @monkeypatch(django.core.wsgi, "get_wsgi_application")
        def _get_wsgi_application(orig, *args, **kwargs):
            # Get the WSGI app
            app = orig(*args, **kwargs)
            # Get or create the Immunio Agent singleton
            agent = get_agent_func()
            # Wrap the WSGI app object with Immunio.
            app = agent.wrap_wsgi_app(app)
            return app



def install_model_importing_hooks(run_hook):
    """These hooks import models."""
    hook_contrib_auth(run_hook)


def install_settings_dependent_hooks(run_hook):
    """These hooks require settings to be configured."""
    try:
        import django
    except ImportError:
        return

    hook_http_request(run_hook)
    hook_url_resolver(run_hook)
    hook_session_middleware(run_hook)
    hook_csrf_middleware(run_hook)
    hook_response_bad_header(run_hook)
    #hook_templates(run_hook)

    # In Django 1.7+, we should also wait to install model-importing hooks
    # until django.setup() is called. Importing models before the app-cache is
    # populated raises warnings in 1.7+ and will be an error in 1.9+.
    if hasattr(django, 'setup'):
        from django.apps import apps

        model_importing_hooks_installed = []

        if apps.ready:
            install_model_importing_hooks(run_hook)
            model_importing_hooks_installed.append(True)
        else:
            original_populate = apps.populate

            @wraps(original_populate)
            def new_populate(installed_apps=None):
                original_populate(installed_apps)
                if not model_importing_hooks_installed:
                    install_model_importing_hooks(run_hook)
                    model_importing_hooks_installed.append(True)

            apps.populate = new_populate
    else:
        # In earlier versions of Django, importing models early was OK.
        install_model_importing_hooks(run_hook)


def hook_http_request(run_hook):
    """
    Hook the Django http request to catch bad signatures when getting
    signed cookies.
    """
    try:
        from django.core.signing import BadSignature
        from django.http.request import (
            HttpRequest,
            RAISE_ERROR,
        )
    except ImportError:
        return

    @monkeypatch(HttpRequest, "get_signed_cookie")
    def _get_signed_cookie(
            orig, self, key, default=RAISE_ERROR, salt='', max_age=None):
        # Save original value of the default
        original_default = default

        try:
            # Call the original get_signed_cookie() but always ask for
            # exceptions to be raised
            return orig(self, key, default=RAISE_ERROR, salt=salt,
                        max_age=max_age)
        except (KeyError, BadSignature) as exc:
            # If we have a bad signature, run the lua hook
            if isinstance(exc, BadSignature):
                run_hook("bad_cookie", {
                    "key": key,
                    "value": self.COOKIES[key],
                    "reason": str(exc),
                })
            # If the original call specified a default,
            # return it instead of raising.
            if original_default is RAISE_ERROR:
                raise
            else:
                return original_default


def hook_url_resolver(run_hook):
    """
    Hook the Django URL resolver so we know which Django view is handling each
    request.
    """
    try:
        import django.core.urlresolvers
    except ImportError:
        return

    @monkeypatch(django.core.urlresolvers.RegexURLResolver, "resolve")
    def _resolve(orig, self, path):
        log.debug(
            "django.core.urlresolvers.RegexURLResolver.resolve(%(path)s)", {
                "path": path,
                })
        view_name = None
        try:
            result = orig(self, path)

            # Build view name from ResolverMatch
            if isinstance(result.func, basestring):
                view_name = result.func
            else:
                # Workaround for tests that might pass a partial.
                if isinstance(result.func, partial):
                    func = result.func.func
                else:
                    func = result.func

                if isinstance(result.func, types.FunctionType):
                    view_name = func.__name__
                else:
                    view_name = func.__class__.__name__ + '.__call__'

                # Prefix view name with module name
                view_name = "%s.%s" % (func.__module__, view_name)
        finally:
            # Send hook
            run_hook("framework_view", {
                "view_name": view_name,
            })
        return result


def hook_contrib_auth(run_hook):
    """
    Hook the Django authentication system to detect login attempts.
    """
    try:
        import django.contrib.auth
        import django.contrib.auth.backends
        import django.contrib.auth.models
        from django.contrib.auth.middleware import AuthenticationMiddleware
    except ImportError:
        return

    def get_username(user):
        """Get a user's username.

        Compatible with both Django 1.4, and custom user models with
        USERNAME_FIELD in Django 1.5+.

        """
        try:
            return user.get_username()
        except AttributeError:
            return getattr(user, 'username', None)

    @monkeypatch("django.contrib.auth.authenticate")
    def _authenticate(orig, **credentials):
        log.debug("django.contrib.auth.authenticate(%(credentials)s)", {
            "credentials": credentials,
            })

        try:
            # Django 1.5 and above use the get_user_model function.
            UserModel = django.contrib.auth.backends.get_user_model()
            username_field = UserModel.USERNAME_FIELD
        except AttributeError:
            # Django 1.4 and below use the User model.
            UserModel = django.contrib.auth.models.User
            username_field = "username"

        username = credentials.get(username_field)

        auth_data = {
            "username": username,
            "is_valid": True
            }

        user = orig(**credentials)
        if user is None:
            auth_data["is_valid"] = False
            auth_data["reason"] = "password"
            if username:
                try:
                    UserModel._default_manager.get_by_natural_key(username)
                except:
                    # Catch everything instead of just DoesNotExist.
                    auth_data["reason"] = "username"
            else:
                auth_data["reason"] = "username"

        run_hook("authenticate", auth_data)
        return user

    @monkeypatch("django.contrib.auth.login")
    def _login(orig, request, user):
        log.debug("django.contrib.auth.login(%(request)s, %(user)s)", {
            "request": request,
            "user": user,
            })

        # Logging in will change our session key. Record the old session_id
        old_session_id = request.session.session_key

        # Call login
        result = orig(request, user)

        session_accessed = request.session.accessed
        try:
            # Django login does not always set request.user; only if request
            # already had a `user` attribute. And it can be called with
            # `user=None`, in which case the user is taken from the request. So
            # we have to be able to take the user from either one, but we can
            # count on it being available from one or the other.
            actual_user = user or request.user
        finally:
            # Accessing request.user will mark the session as accessed, thus
            # triggering Vary: Cookie on the response. We need to reset this.
            request.session.accessed = session_accessed

        # Send hook
        run_hook("framework_login", {
            "user_id": actual_user.pk,
            "username": get_username(actual_user),
            # Use the SHA1 of the session_id so the VM does not have access
            # to the actual real session_id.
            "old_session_id": sha1hash(old_session_id),
            "new_session_id": sha1hash(request.session.session_key),
        })
        return result

    @monkeypatch("django.contrib.auth.logout")
    def _logout(orig, request):
        log.debug("django.contrib.auth.logout(%(request)s)", {
            "request": request,
            })

        # Logging out will change our session key. Record the old session_id
        old_session_id = request.session.session_key
        result = orig(request)
        # Send hook
        run_hook("framework_logout", {
            # Use the SHA1 of the session_id so the VM does not have access
            # to the actual real session_id.
            "old_session_id": sha1hash(old_session_id),
            "new_session_id": sha1hash(request.session.session_key),
        })
        return result

    @monkeypatch("django.contrib.auth.get_user")
    def _get_user(orig, request):
        log.debug("django.contrib.auth.get_user(%(request)s)", {
            "request": request,
            })

        user = orig(request)

        # Only send hook if user is not anonymous, otherwise an user_id
        # and username are None resulting in an empty framework_user dict.
        if not user.is_anonymous():
            run_hook("framework_user", {
                "user_id": user.pk,
                "username": get_username(user),
            })

        return user

    @monkeypatch(AuthenticationMiddleware, "process_request")
    def _process_request(orig, self, request):
        """
        We don't actually send any hooks from here - we just need to access
        `request.user` to activate the lazy object to trigger the
        `get_user()` hook above.
        """
        log.debug("AuthenticationMiddleware.process_request(%(request)s)", {
            "request": request,
            })

        result = orig(self, request)

        # If no session store is used, there may be no `request.session`.
        if hasattr(request, "session") and request.session is not None:
            session_accessed = request.session.accessed

        try:
            # Don't do anything with result, just trigger the LazyObject
            request.user
        finally:
            # Accessing request.user will mark the session as accessed, thus
            # triggering Vary: Cookie on the response. We need to reset this.
            if hasattr(request, "session") and request.session is not None:
                request.session.accessed = session_accessed

        return result


def hook_session_middleware(run_hook):
    """
    Hook the session middleware system to determine the active session for each
    request and to detect potential session tampering.
    """
    try:
        from django.contrib.sessions.middleware import SessionMiddleware
    except ImportError:
        return

    @monkeypatch(SessionMiddleware, "process_request")
    def _process_request(orig, self, request):
        log.debug("SessionMiddleware.process_request(%(request)s)", {
            "request": request,
            })

        result = orig(self, request)
        try:
            # Get session_key from session
            session_key = request.session.session_key
        except AttributeError:
            session_key = None

        # Send hook
        run_hook("framework_session", {
            # Use the SHA1 of the session_id so the VM does not have access
            # to the actual real session_id.
            "session_id": sha1hash(session_key),
        })
        return result


def hook_csrf_middleware(run_hook):
    """
    Hook the CSRF middleware system to determine the CSRF status for each
    request. This also works with the `csrf_protect` decorator since it
    just uses the middleware.
    """
    try:
        from django.middleware.csrf import CsrfViewMiddleware
    except ImportError:
        return

    @monkeypatch(CsrfViewMiddleware, "_accept")
    def _accept(orig, self, request):
        log.debug("CsrfViewMiddleware._accept(%(request)s)", {
            "request": request,
            })

        # Send hook
        run_hook("framework_csrf_check", {
            "valid": True,
        })
        return orig(self, request)

    @monkeypatch(CsrfViewMiddleware, "_reject")
    def _reject(orig, self, request, reason):
        if isinstance(reason, unicode):
            reason = reason.encode("utf-8")

        log.debug("CsrfViewMiddleware._reject(%(request)s, %(reason)s)", {
            "request": request,
            "reason": reason,
            })

        # Send hook
        run_hook("framework_csrf_check", {
            "valid": False,
            "reason": reason,
        })
        return orig(self, request, reason)


def hook_templates(run_hook):
    """
    Hook the Django template system to monitor output for XSS exploits.
    """
    try:
        from django.template.base import (
            Template,
            FilterExpression,
        )
        from django.utils.safestring import (
            SafeData,
        )
    except ImportError:
        return

    # Keep a copy of the original method
    original_init = Template.__init__

    # Define our replacement method
    def __init__(self, template_string, *args, **kwargs):
        if isinstance(template_string, unicode):
            template_string = template_string.encode('utf-8')
        template_sha = sha1(template_string).hexdigest()

        # Extract origin and name if present
        origin = None
        name = None
        if len(args) > 0:
            origin = args[0]
        if len(args) > 1:
            name = args[1]
        if "origin" in kwargs:
            origin = kwargs["origin"]
        if "name" in kwargs:
            name = kwargs["name"]

        # `origin`, if specified, is an object with a `name` attribute.
        origin = getattr(origin, "name", None)

        # Patch the render method inside the __init__ context so we can
        # include the template id.
        original_render = self.render

        def render(context):
            log.debug("Template.render(%(context)s)", {
                "context": context,
                })

            run_hook("template_render", {
                "template_sha": template_sha,
                "context": context,
            })

            try:
                rendered = original_render(context)

                result = run_hook("template_render_done", {
                    "template_sha": template_sha,
                    "rendered": rendered,
                })
            except Exception as exc:
                run_hook(
                    "template_render_exception",
                    # The comment on the next line keeps a
                    # stack-frame-introspecting Django test happy.
                    {"exception": str(exc)},  # raise BrokenException
                )
                raise

            # If a new render was provided in the hook response, use it instead
            return result.get("rendered", rendered)

        # Replace the original render function.
        self.render = render

        run_hook("template_load", {
            "template_sha": template_sha,
            "template_string": template_string,
            "origin": origin,
            "name": name,
        })

        return original_init(self, template_string, *args, **kwargs)

    # Replace original with our version
    Template.__init__ = __init__

    original_resolve = FilterExpression.resolve

    def resolve(self, context, ignore_failures=False):
        captured_values = []

        # inject a fake no-op filter at the head of the chain, to capture the
        # original variable value
        def capture(val):
            captured_values.append(val)
            return val

        self.filters.insert(0, (capture, []))
        try:
            rendered = original_resolve(self, context, ignore_failures)
        finally:
            self.filters.pop(0)

        raw = captured_values[0] if captured_values else None

        result = run_hook("template_render_var", {
            "filter_expression": self.token,
            "raw": raw,
            "rendered": rendered,
            "marked_safe": isinstance(rendered, SafeData),
        })

        # If a new render was provided in the hook response, use it instead
        return result.get("rendered", rendered)

    FilterExpression.resolve = resolve


def hook_settings(run_hook):
    try:
        import django.conf
    except ImportError:
        return

    settings_dependent_hooks_installed = []

    # Hook the settings module
    settings = django.conf.settings

    # If settings are already configured, install setting-dependent hooks now
    if settings.configured:
        install_settings_dependent_hooks(run_hook)
        settings_dependent_hooks_installed.append(True)

    # Normally, the initial settings configuration looks like a bunch of
    # individual changes. Share them up so we get a single hook called.
    shared = {
        "settings": {},
        "collecting": False,
        }

    # Hook the settings object to catch attribute changes
    orig_set_attr = django.conf.BaseSettings.__setattr__

    def new_set_attr(bound_self, name, value):
        log.debug(
            "django.conf.BaseSettings.__setattr__(%(name)s, %(value)s)", {
                "name": name,
                "value": value,
                })
        if shared["collecting"]:
            # Don't fire change hook, collect instead
            shared["settings"][name] = value
        else:
            # Not collecting, fire the change hook
            run_hook("change_setting", {"name": name, "value": value})

        return orig_set_attr(bound_self, name, value)
    setattr(django.conf.BaseSettings, "__setattr__", new_set_attr)

    orig_setup = settings._setup

    def new_setup(*args, **kwargs):
        log.debug(
            "settings._setup(%(args)s, %(kwargs)s)", {
                "args": args,
                "kwargs": kwargs,
                })
        # Set up collecting
        shared["settings"] = {}
        shared["collecting"] = True
        try:
            orig_setup(*args, **kwargs)
            run_hook("load_settings", {"settings": shared["settings"]})
        finally:
            shared["settings"] = {}
            shared["collecting"] = False
        if not settings_dependent_hooks_installed:
            install_settings_dependent_hooks(run_hook)
            settings_dependent_hooks_installed.append(True)
    settings.__dict__["_setup"] = new_setup

    orig_configure = settings.configure

    def new_configure(*args, **kwargs):
        log.debug(
            "settings.configure(%(args)s, %(kwargs)s)", {
                "args": args,
                "kwargs": kwargs,
                })
        # Set up collecting
        shared["settings"] = {}
        shared["collecting"] = True
        try:
            orig_configure(*args, **kwargs)
            run_hook("configure_settings", {"settings": shared["settings"]})
        finally:
            shared["settings"] = {}
            shared["collecting"] = False
        if not settings_dependent_hooks_installed:
            install_settings_dependent_hooks(run_hook)
            settings_dependent_hooks_installed.append(True)
    settings.__dict__["configure"] = new_configure


def hook_response_bad_header(run_hook):
    """
    Hook the Django exception thrown from Response when headers are invalid.
    """
    try:
        from django.http.response import HttpResponseBase, BadHeaderError
    except ImportError:
        try:
            # django 1.4 doesn't have django.http.response
            from django.http import HttpResponse as HttpResponseBase
            from django.http import BadHeaderError
        except ImportError:
            # No django
            return

    @monkeypatch(HttpResponseBase, "__setitem__")
    def __setitem__(orig, self, header, value):
        log.debug("HttpResponseBase.__setitem__(%(header)s, %(value)s)", {
            "header": header,
            "value": value,
            })
        try:
            return orig(self, header, value)
        except (BadHeaderError, UnicodeError) as exc:
            # Send hook
            run_hook("framework_bad_response_header", {
                "header": header,
                "value": value,
                "reason": str(exc),
            })
            raise  # re-raise exception back to application after we're done
