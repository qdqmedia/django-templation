from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from templation.locals import thread_locals


@login_required
def index(request, pk):
    thread_locals.resource = pk
    return render_to_response('tests/index.html', {'name': 'John'})
