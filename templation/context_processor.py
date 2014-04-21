def templation_info(request):
    return {
        'templation_view': getattr(request, '_templation_view', None),
        'templation_template': getattr(request, '_templation_template', None),
    }
