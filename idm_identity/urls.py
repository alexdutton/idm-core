from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_nested import routers

import idm_identity.views
import idm_identity.gender.views
import idm_identity.name.views
import idm_identity.identifier.views
import idm_identity.attestation.views
import idm_identity.org_relationship.views
import idm_identity.nationality.views

router = routers.DefaultRouter()
router.register('identity', idm_identity.views.IdentityViewSet)
router.register('gender', idm_identity.gender.views.GenderViewSet)
router.register('country', idm_identity.nationality.views.CountryViewSet)
router.register('affiliation-type', idm_identity.org_relationship.views.AffiliationTypeViewSet)
router.register('role-type', idm_identity.org_relationship.views.RoleTypeViewSet)
router.register('identifier-type', idm_identity.identifier.views.IdentifierTypeViewSet)
router.register('unit', idm_identity.org_relationship.views.UnitViewSet)

identity_router = routers.NestedSimpleRouter(router, r'identity', lookup='identity')
identity_router.register('nationality', idm_identity.nationality.views.NationalityViewSet, base_name='identity-nationality')
identity_router.register('affiliation', idm_identity.org_relationship.views.AffiliationViewSet, base_name='identity-affiliation')
identity_router.register('role', idm_identity.org_relationship.views.RoleViewSet, base_name='identity-role')
identity_router.register('source-document', idm_identity.attestation.views.SourceDocumentViewSet, base_name='identity-source-document')
identity_router.register('name', idm_identity.name.views.NameViewSet, base_name='identity-name')


router.register('name', idm_identity.name.views.NameViewSet)
router.register('nationality', idm_identity.nationality.views.NationalityViewSet)
router.register('source-document', idm_identity.attestation.views.SourceDocumentViewSet)
router.register('attestation', idm_identity.attestation.views.AttestationViewSet)
router.register('affiliation', idm_identity.org_relationship.views.AffiliationViewSet)
router.register('role', idm_identity.org_relationship.views.RoleViewSet)

admin.autodiscover()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(identity_router.urls)),
    url(r'^admin/', admin.site.urls),

]
