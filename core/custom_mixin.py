from django.http import Http404

class NoGetMixin:
    template_name = 'blank.html'
    def get(self, request, *args, **kwargs):
        raise Http404()

class CustomPaginationMixin:
    def get_paginate_by(self, queryset):
        print('asdasdasd')
        print(self.request.GET.get("paginate_by", self.paginate_by))
        return self.request.GET.get("paginate_by", self.paginate_by)