class NoGetMixin:
    # template_name = 'blank.html'
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)