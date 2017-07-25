from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.NameListView.as_view(), name='name-list'),
    url(r'^(?P<pk>[1-9][0-9]*)/$', views.NameDetailView.as_view(), name='name-detail'),
]