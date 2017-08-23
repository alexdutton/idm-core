from django.conf.urls import url

from . import views

uuid_re = '[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}'

urlpatterns = [

    url(r'^email/$',
        views.EmailListView.as_view(), name='email-list-self'),
    url(r'^(?P<identity_type>[a-z-]+)/(?P<identity_id>' + uuid_re + ')/email/$',
        views.EmailListView.as_view(), name='email-list'),

    url(r'^online-account/$',
        views.OnlineAccountListView.as_view(), name='online-account-list-self'),
    url(r'^(?P<identity_type>[a-z-]+)/(?P<identity_id>' + uuid_re + ')/online-account/$',
        views.OnlineAccountListView.as_view(), name='online-account-list'),

    url(r'^telephone/$',
        views.TelephoneListView.as_view(), name='telephone-list-self'),
    url(r'^(?P<identity_type>[a-z-]+)/(?P<identity_id>' + uuid_re + ')/telephone/$',
        views.TelephoneListView.as_view(), name='telephone-list'),

    url(r'^address/$',
        views.AddressListView.as_view(), name='address-list-self'),
    url(r'^(?P<identity_type>[a-z-]+)/(?P<identity_id>' + uuid_re + ')/address/$',
        views.AddressListView.as_view(), name='address-list'),
]
