
class SameIdentityMixin(object):
    def get_queryset(self):
        return super().get_queryset().filter(identity_id=self.request.user.identity_id)
