

def getvars(request):
    """
    Builds a GET variables string to be uses in template links like pagination
    when persistence of the GET vars is needed.
    """
    variables = request.GET.copy()

    if 'page' in variables:
        del variables['page']

    return {'getvars': '&{0}'.format(variables.urlencode())}

def getvars_perpage(request):

    variables = request.GET.copy()
    if 'per_page' in variables:
        del variables['per_page']

    return {'getvars_perpage': '&{0}'.format(variables.urlencode())}