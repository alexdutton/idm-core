from django.conf.urls import include, url
from rest_framework_nested import routers

import idm_core.attestation.views
import idm_core.contact.views
import idm_core.identifier.views
import idm_core.name.views
import idm_core.nationality.views
import idm_core.relationship.views
import idm_core.organization.api
import idm_core.person.views
import idm_core.application.views
import idm_core.statistics.views

router = routers.DefaultRouter()
router.register('identity', idm_core.identity.views.IdentityViewSet, 'identity')
router.register('person', idm_core.person.views.PersonViewSet, base_name='person')
router.register('organization', idm_core.organization.api.OrganizationViewSet, base_name='organization')
router.register('country', idm_core.nationality.views.CountryViewSet)
router.register('affiliation-type', idm_core.organization.api.AffiliationTypeViewSet)
router.register('role-type', idm_core.organization.api.RoleTypeViewSet)
router.register('identifier-type', idm_core.identifier.views.IdentifierTypeViewSet)
router.register('application', idm_core.application.views.ApplicationViewSet)
router.register('organization', idm_core.organization.api.OrganizationViewSet)


person_router = routers.NestedSimpleRouter(router, r'person', lookup='identity')
person_router.register('nationality', idm_core.nationality.views.NationalityViewSet, base_name='identity-nationality')
person_router.register('affiliation', idm_core.organization.api.AffiliationViewSet, base_name='identity-affiliation')
person_router.register('role', idm_core.organization.api.RoleViewSet, base_name='identity-role')
person_router.register('source-document', idm_core.attestation.views.SourceDocumentViewSet, base_name='identity-source-document')
person_router.register('name', idm_core.name.views.NameViewSet, base_name='identity-name')
person_router.register('identifier', idm_core.identifier.views.IdentifierViewSet, base_name='identity-identifier')
person_router.register('attestable', idm_core.attestation.views.AttestableViewSet, base_name='identity-attestable')
person_router.register('attestable', idm_core.attestation.views.AttestableViewSet, base_name='identity-attestable')



router.register('name', idm_core.name.views.NameViewSet, base_name='name')
router.register('nationality', idm_core.nationality.views.NationalityViewSet)
router.register('source-document', idm_core.attestation.views.SourceDocumentViewSet)
router.register('attestation', idm_core.attestation.views.AttestationViewSet)
router.register('affiliation', idm_core.organization.api.AffiliationViewSet)
router.register('role', idm_core.organization.api.RoleViewSet)
router.register('identifier', idm_core.identifier.views.IdentifierViewSet)
router.register('email', idm_core.contact.views.EmailViewSet)
router.register('telephone', idm_core.contact.views.TelephoneViewSet)
router.register('address', idm_core.contact.views.AddressViewSet)
router.register('online-account', idm_core.contact.views.OnlineAccountViewSet, base_name='online-account')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(person_router.urls)),
    url(r'^statistics/$', idm_core.statistics.views.StatisticsView.as_view()),
]