class NoGetMixin:
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)