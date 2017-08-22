from django.conf.urls import url

from . import views

uuid_re = '[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}'

urlpatterns = [
    url(r'^name/$',
        views.NameListView.as_view(), name='name-list-self'),
    url(r'^(?P<identity_type>[a-z-]+)/(?P<identity_id>' + uuid_re + ')/name/$',
        views.NameListView.as_view(), name='name-list'),
    url(r'^name/(?P<pk>[1-9][0-9]*)/$', views.NameDetailView.as_view(), name='name-detail'),
    url(r'^name/new:(?P<context>[\w-]+)/$',
        views.NameCreateView.as_view(), name='name-create-self'),
    url(r'^(?P<identity_type>[a-z-]+)/(?P<identity_id>' + uuid_re + ')/name/new:(?P<context>[\w-]+)/$',
        views.NameCreateView.as_view(), name='name-create'),
]