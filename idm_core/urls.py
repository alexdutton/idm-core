from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = [
    url(r'^', include('idm_core.selfservice.urls', 'selfservice')),
    url(r'^organization/', include('idm_core.organization.urls', 'organization')),
    url(r'^api/', include('idm_core.api_urls', 'api')),
    url(r'^admin/', admin.site.urls),
    url(r'^oidc/', include('oidc_auth.urls')),
]
