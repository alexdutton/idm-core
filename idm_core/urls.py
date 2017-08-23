from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import logout

from idm_core.organization.views import PersonAffiliationListView

admin.autodiscover()

urlpatterns = [
    url(r'^', include('idm_core.selfservice.urls', 'selfservice')),
    url(r'^', include('idm_core.contact.urls', 'contact')),
    url(r'^', include('idm_core.image.urls', 'image')),
    url(r'^', include('idm_core.attestation.urls', 'attestation')),
    url(r'^affiliation/$', PersonAffiliationListView.as_view(), name='person-affiliation-list'),
    url(r'^', include('idm_core.name.urls', 'name')),
    url(r'^organization/', include('idm_core.organization.urls', 'organization')),
    url(r'^api/', include('idm_core.api_urls', 'api')),
    url(r'^admin/', admin.site.urls),
    url(r'^oidc/', include('oidc_auth.urls')),
    url(r'^logout/$', logout, name='logout'),
]
