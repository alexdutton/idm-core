from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_nested import routers

import idm_core.views
import idm_core.name.views
import idm_core.identifier.views
import idm_core.attestation.views
import idm_core.org_relationship.views
import idm_core.nationality.views

router = routers.DefaultRouter()
router.register('identity', idm_core.views.IdentityViewSet)
router.register('country', idm_core.nationality.views.CountryViewSet)
router.register('affiliation-type', idm_core.org_relationship.views.AffiliationTypeViewSet)
router.register('role-type', idm_core.org_relationship.views.RoleTypeViewSet)
router.register('identifier-type', idm_core.identifier.views.IdentifierTypeViewSet)
router.register('unit', idm_core.org_relationship.views.UnitViewSet)

identity_router = routers.NestedSimpleRouter(router, r'identity', lookup='identity')
identity_router.register('nationality', idm_core.nationality.views.NationalityViewSet, base_name='identity-nationality')
identity_router.register('affiliation', idm_core.org_relationship.views.AffiliationViewSet, base_name='identity-affiliation')
identity_router.register('role', idm_core.org_relationship.views.RoleViewSet, base_name='identity-role')
identity_router.register('source-document', idm_core.attestation.views.SourceDocumentViewSet, base_name='identity-source-document')
identity_router.register('name', idm_core.name.views.NameViewSet, base_name='identity-name')


router.register('name', idm_core.name.views.NameViewSet)
router.register('nationality', idm_core.nationality.views.NationalityViewSet)
router.register('source-document', idm_core.attestation.views.SourceDocumentViewSet)
router.register('attestation', idm_core.attestation.views.AttestationViewSet)
router.register('affiliation', idm_core.org_relationship.views.AffiliationViewSet)
router.register('role', idm_core.org_relationship.views.RoleViewSet)

admin.autodiscover()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(identity_router.urls)),
    url(r'^admin/', admin.site.urls),

]
