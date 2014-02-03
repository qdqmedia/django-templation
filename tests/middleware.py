from django.shortcuts import get_object_or_404
from templation.settings import get_resource_model, REQUEST_RESOURCE_NAME


class TestMiddleware(object):
    def process_request(self, request):
        pk = request.path.split('/')[1]
        myresource = get_object_or_404(get_resource_model(), pk=pk)
        setattr(request, REQUEST_RESOURCE_NAME, myresource)
