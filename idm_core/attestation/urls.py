from django.conf.urls import url

from . import views

uuid_re = '[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}'

urlpatterns = [
    url(r'^attestation/$',
        views.SourceDocumentListView.as_view(), name='source-document-list-self'),
    url(r'^(?P<identity_type>[a-z-]+)/(?P<identity_id>' + uuid_re + ')/attestation/$',
        views.SourceDocumentListView.as_view(), name='source-document-list'),

    url(r'^attestation/new/$',
        views.SourceDocumentWizardView.as_view(), name='source-document-new-self'),
    url(r'^(?P<identity_type>[a-z-]+)/(?P<identity_id>' + uuid_re + ')/attestation/new/$',
        views.SourceDocumentWizardView.as_view(), name='source-document-new'),

]