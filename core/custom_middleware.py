from django.http import HttpResponseNotAllowed
from django.template import RequestContext
from django.template import loader
from django.utils.deprecation import MiddlewareMixin

class HttpResponseNotAllowedMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if isinstance(response, HttpResponseNotAllowed):
            response.content = loader.render_to_string("405.html")
        return response    