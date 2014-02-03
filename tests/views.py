from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


@login_required
def index(request, pk):
    return render_to_response('tests/index.html', {'name': 'John'})
