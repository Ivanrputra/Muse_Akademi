from django.http import Http404

class NoGetMixin:
    template_name = 'blank.html'
    def get(self, request, *args, **kwargs):
        raise Http404()