from django.conf.urls import url

from . import views

uuid_re = r'[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}'

urlpatterns = [
    url(r'^$', views.OrganizationListView.as_view(), name='index'),

    url(r'^(?P<pk>' + uuid_re + ')/$',
        views.OrganizationDetailView.as_view(), name='detail'),

    url(r'^(?P<organization_pk>' + uuid_re + ')/affiliation/$',
        views.AffiliationListView.as_view(), name='affiliation-list'),

    url(r'^(?P<organization_pk>' + uuid_re + ')/affiliation/new/$',
        views.AffiliationCreateView.as_view(), name='affiliation-create'),

    url(r'^(?P<organization_pk>' + uuid_re + ')/affiliation/invite/$',
        views.AffiliationInviteView.as_view(), name='affiliation-invite'),

    url(r'^(?P<organization_pk>' + uuid_re + ')/affiliation/(?P<pk>[1-9]\d*)/$',
        views.AffiliationUpdateView.as_view(), name='affiliation-update'),
]