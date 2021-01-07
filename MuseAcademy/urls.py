"""MuseAcademy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns 
from django.views.static import serve

from apps.app.views import change_language

def serve_unprotected(request,path):
    return serve(
        request, path, document_root=settings.MEDIA_ROOT,
        show_indexes=False
    )

# def serve_protected(request,path):
#     return serve(
#         request, path, document_root=settings.PROTECTED_MEDIA_ROOT,
#         show_indexes=False
#     )

urlpatterns = [
    path('', include('pwa.urls')),  # You MUST use an empty string as the URL prefix
    path('change_language/', change_language, name='change_language'),
        # Library URL
    path('oauth/', include('social_django.urls', namespace='social')),
    path('summernote/', include('django_summernote.urls')),
    path("select2/", include("django_select2.urls")),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),

    path('',        include('apps.app.urls')),
    path('',        include('apps.user.urls')),
    path('api/',    include('apps.api.urls')),
    path('mentor/', include('apps.mentor.urls')),
    path('payment/',include('apps.payment.urls')),
    

    # languange default is id
    prefix_default_language=False
)
if (settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.PROTECTED_MEDIA_URL, document_root=settings.PROTECTED_MEDIA_ROOT)
else:
    urlpatterns.append(path('media/<path:path>',serve_unprotected,name="serve-unprotected"),) 
