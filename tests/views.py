from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from templation.settings import get_resource_model, REQUEST_RESOURCE_NAME


@login_required
def index(request, pk):
    myresource = get_object_or_404(get_resource_model(), pk=pk)
    setattr(request, REQUEST_RESOURCE_NAME, myresource)
    return render_to_response('tests/index.html', {'name': 'John'})
