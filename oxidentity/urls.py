from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_nested import routers

import oxidentity.views
import oxidentity.gender.views
import oxidentity.name.views
import oxidentity.identifier.views
import oxidentity.attestation.views
import oxidentity.org_relationship.views
import oxidentity.nationality.views

router = routers.DefaultRouter()
router.register('person', oxidentity.views.PersonViewSet)
router.register('gender', oxidentity.gender.views.GenderViewSet)
router.register('country', oxidentity.nationality.views.CountryViewSet)
router.register('affiliation-type', oxidentity.org_relationship.views.AffiliationTypeViewSet)
router.register('role-type', oxidentity.org_relationship.views.RoleTypeViewSet)
router.register('identifier-type', oxidentity.identifier.views.IdentifierTypeViewSet)
router.register('unit', oxidentity.org_relationship.views.UnitViewSet)

person_router = routers.NestedSimpleRouter(router, r'person', lookup='person')
person_router.register('nationality', oxidentity.nationality.views.NationalityViewSet, base_name='person-nationality')
person_router.register('affiliation', oxidentity.org_relationship.views.AffiliationViewSet, base_name='person-affiliation')
person_router.register('role', oxidentity.org_relationship.views.RoleViewSet, base_name='person-role')
person_router.register('source-document', oxidentity.attestation.views.SourceDocumentViewSet, base_name='person-source-document')


router.register('name', oxidentity.name.views.NameViewSet)
router.register('nationality', oxidentity.nationality.views.NationalityViewSet)
router.register('source-document', oxidentity.attestation.views.SourceDocumentViewSet)
router.register('attestation', oxidentity.attestation.views.AttestationViewSet)
router.register('affiliation', oxidentity.org_relationship.views.AffiliationViewSet)
router.register('role', oxidentity.org_relationship.views.RoleViewSet)

admin.autodiscover()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(person_router.urls)),
    url(r'^admin/', admin.site.urls),

]
