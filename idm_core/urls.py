from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = [
    url(r'^', include('idm_core.selfservice.urls', 'selfservice')),
    url(r'^api/', include('idm_core.api_urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^oidc/', include('oidc_auth.urls')),
]
