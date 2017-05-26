from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^source-document/$', views.SourceDocumentListView.as_view, name='source-document-list'),
]