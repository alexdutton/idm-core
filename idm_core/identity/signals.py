from django.dispatch import Signal

pre_merge = Signal(['target', 'others', 'other_ids'])
post_merge = Signal(['target', 'others', 'other_ids'])
