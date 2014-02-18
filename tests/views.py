from django.shortcuts import render_to_response
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from templation.locals import thread_locals
from templation.views import ResourceStoreMixin
from .models import MyResource


def index(request, pk):
    thread_locals.resource = pk
    return render_to_response('index.html', {'name': 'John'})


class IndexView(ResourceStoreMixin, DetailView):
    template_name = 'index.html'
    model = MyResource


class FailView(ResourceStoreMixin, DetailView):
    template_name = 'fail.html'
    model = MyResource


class ExtendedView(ResourceStoreMixin, DetailView):
    template_name = 'extension_and_inclusion.html'
    model = MyResource


class PublicView(TemplateView):
    template_name = 'load_ok.html'
