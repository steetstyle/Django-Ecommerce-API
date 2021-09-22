from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views import defaults as default_views
from django.http import HttpResponseRedirect

#wagtail 
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

import django_cas_ng.views

from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet
from wagtail.images.views.serve import ServeView

from core.views import AuthProfileDetail


# Create the router. "wagtailapi" is the URL namespace
wagtail_api_router = WagtailAPIRouter('wagtailapi')

# Add the three endpoints using the "register_endpoint" method.
# The first parameter is the name of the endpoint (eg. pages, images). This
# is used in the URL of the endpoint
# The second parameter is the endpoint class that handles the requests
wagtail_api_router.register_endpoint('pages', PagesAPIViewSet)
wagtail_api_router.register_endpoint('images', ImagesAPIViewSet)
wagtail_api_router.register_endpoint('documents', DocumentsAPIViewSet)

def redirect_to_profile(request):
    return HttpResponseRedirect(redirect_to="http://localhost:9000/auth/profile")

urlpatterns = [
    path('admin/', admin.site.urls),
    #cas
    path('accounts/login', django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
    path('accounts/logout', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),
    path('accounts/callback', django_cas_ng.views.CallbackView.as_view(), name='cas_ng_proxy_callback'),
    #salesman
    path('sales/', include('salesman.urls')),
    # core urls
    path('accounts/profile', AuthProfileDetail.as_view({'get': 'retrieve'}), name='cas_ng_auth_profile'),
    #wagtail
    re_path(r'^images/([^/]*)/(\d*)/([^/]*)/[^/]*$', ServeView.as_view(), name='wagtailimages_serve'),
    path('api/v2/', wagtail_api_router.urls),
    re_path(r'^cms/', include(wagtailadmin_urls)),
    re_path(r'^documents/', include(wagtaildocs_urls)),
    re_path(r'^pages/', include(wagtail_urls)),

    #app
    path('payments/', include('payments.urls')), # new
    path('qrtable/', include('qrtable.urls')), # new
    #path('producer/', include('project.producer.urls')),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
