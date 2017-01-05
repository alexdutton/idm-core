import collections
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView

from idm_core.identity.models import Identity


class StatisticsView(APIView):
    def get(self, request):
        recursive_defaultdict = lambda: collections.defaultdict(recursive_defaultdict)
        data = recursive_defaultdict()
        for result in Identity.objects.values('type_id', 'state').annotate(count=Count('*')):
            data[result['type_id'].title()][result['state']] = result['count']
        return Response(data)