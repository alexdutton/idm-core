from django.conf.urls import url

from . import views

uuid_re = '[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}'

urlpatterns = [
    url(r'^image/$',
        views.ImageListView.as_view(), name='image-list-self'),
    url(r'^(?P<identity_type>[a-z-]+)/(?P<identity_id>' + uuid_re + ')/image/$',
        views.ImageListView.as_view(), name='image-list'),
    url(r'^image/(?P<pk>' + uuid_re + ')/$',
        views.ImageDetailView.as_view(), name='image-detail'),
    url(r'^image/new:(?P<context>[\w-]+)/$',
        views.ImageCreateView.as_view(), name='image-create-self'),
    url(r'^(?P<identity_type>[a-z-]+)/(?P<identity_id>' + uuid_re + ')/image/new:(?P<context>[\w-]+)/$',
        views.ImageCreateView.as_view(), name='image-create'),

    url(r'^image/file/(?P<pk>' + uuid_re + ')/$',
        views.ImageFileView.as_view(), name='image-file'),
]