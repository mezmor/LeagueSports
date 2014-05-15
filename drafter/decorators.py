from functools import wraps
from django.utils.decorators import available_attrs
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
def commish_required(redirect_view=None):
    def decorator(view_func):
        #@wraps(view_func, assigned=available_attrs(view_func))
        def _wrapper(request, *args, **kwargs):
            if int(kwargs['league_id']) in request.user.managed_leagues.values_list('id', flat=True):
                return view_func(request, *args, **kwargs)
            if redirect_view:
                return redirect('drafter.views.league', **kwargs)
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return _wrapper
    return decorator