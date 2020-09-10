from django.http import HttpResponseNotAllowed
from django.template import RequestContext
from django.template import loader
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse,reverse_lazy
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from django.shortcuts import redirect
from django.contrib import messages   

class HttpResponseNotAllowedMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated and not request.user.has_usable_password() and resolve(request.path_info).url_name != 'password_change':
        # if not request.user.has_usable_password():
            # print("password tidak usable")
            # current_url = resolve(request.path_info).url_name
            # print(resolve(request.path_info).url_name)
            # return HttpResponseRedirect(reverse('user:password_change'))
            messages.warning(request,"Segera perbarui password anda")
            return redirect('user:password_change')
        if isinstance(response, HttpResponseNotAllowed):
            response.content = loader.render_to_string("405.html")
        return response    