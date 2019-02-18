
#Not used but could be useful
#Custom middleware
from django.conf import settings
from django.shortcuts import redirect

EXEMPT_URLS = [settings.HOME_URL.lstrip('/')]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [url for url in settings.LOGIN_EXEMPT_URLS]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')
        login_path = (
            'account/login/',
            'account/register/',
        )
        if not request.user.is_authenticated:
            # Temporary fix, must find solution cause this is a big vulnerability
            if path.startswith("account/password_reset/confirm/") or path.startswith("account/register/activate") or path.startswith("home/post"):
                return None
            elif not path in EXEMPT_URLS:
                return redirect(settings.HOME_URL)

        elif request.user.is_authenticated and path in login_path:
            return redirect(settings.ALREADY_LOGGED_URL)
