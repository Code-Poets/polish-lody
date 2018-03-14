from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.utils.translation import LANGUAGE_SESSION_KEY


@login_required
def dashboard(request):
    return render(
        request,
        'dashboard/dashboard.html'
    )


def languageChange(request):
    language = request.LANGUAGE_CODE
    if language == 'en':
        language = 'pl'
    else:
        language = 'en'
    request.session[LANGUAGE_SESSION_KEY] = language

    try:
        return redirect(request.META['HTTP_REFERER'])
    except:
        return HttpResponseRedirect("../")
