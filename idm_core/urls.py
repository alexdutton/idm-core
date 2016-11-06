from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_nested import routers

import idm_core.attestation.views
import idm_core.identifier.views
import idm_core.name.views
import idm_core.nationality.views
import idm_core.org_relationship.views
import idm_core.person.views

router = routers.DefaultRouter()
router.register('person', idm_core.person.views.PersonViewSet)
router.register('country', idm_core.nationality.views.CountryViewSet)
router.register('affiliation-type', idm_core.org_relationship.views.AffiliationTypeViewSet)
router.register('role-type', idm_core.org_relationship.views.RoleTypeViewSet)
router.register('identifier-type', idm_core.identifier.views.IdentifierTypeViewSet)
router.register('unit', idm_core.org_relationship.views.UnitViewSet)

person_router = routers.NestedSimpleRouter(router, r'person', lookup='person')
person_router.register('nationality', idm_core.nationality.views.NationalityViewSet, base_name='person-nationality')
person_router.register('affiliation', idm_core.org_relationship.views.AffiliationViewSet, base_name='person-affiliation')
person_router.register('role', idm_core.org_relationship.views.RoleViewSet, base_name='person-role')
person_router.register('source-document', idm_core.attestation.views.SourceDocumentViewSet, base_name='person-source-document')
person_router.register('name', idm_core.name.views.NameViewSet, base_name='person-name')
person_router.register('identifier', idm_core.identifier.views.IdentifierViewSet, base_name='person-identifier')


router.register('name', idm_core.name.views.NameViewSet)
router.register('nationality', idm_core.nationality.views.NationalityViewSet)
router.register('source-document', idm_core.attestation.views.SourceDocumentViewSet)
router.register('attestation', idm_core.attestation.views.AttestationViewSet)
router.register('affiliation', idm_core.org_relationship.views.AffiliationViewSet)
router.register('role', idm_core.org_relationship.views.RoleViewSet)
router.register('identifier', idm_core.identifier.views.IdentifierViewSet)

admin.autodiscover()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(person_router.urls)),
    url(r'^admin/', admin.site.urls),

]
