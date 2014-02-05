from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from templation.locals import thread_locals
from templation.views import ResourceStoreMixin
from .models import MyResource


@login_required
def index(request, pk):
    thread_locals.resource = pk
    return render_to_response('tests/index.html', {'name': 'John'})


class IndexView(ResourceStoreMixin, DetailView):
    template_name = 'tests/index.html'
    model = MyResource
