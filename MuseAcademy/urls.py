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

# def serve_unprotected(request,path):
#     return serve(
#         request, path, document_root=settings.MEDIA_ROOT,
#         show_indexes=False
#     )

# def serve_protected(request,path):
#     return serve(
#         request, path, document_root=settings.PROTECTED_MEDIA_ROOT,
#         show_indexes=False
#     )


urlpatterns = [
    path('admin/', admin.site.urls),

    path('',        include('apps.app.urls')),
    path('',        include('apps.user.urls')),
    path('api/',    include('apps.api.urls')),
    path('mentor/', include('apps.mentor.urls')),
    # path('payment/',include('apps.payment.urls')),
    path('management/',include('apps.management.urls')),

    path('oauth/', include('social_django.urls', namespace='social')),

]
if (settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.PROTECTED_MEDIA_URL, document_root=settings.PROTECTED_MEDIA_ROOT)
    # urlpatterns.append(path('media/<path:path>',serve_unprotected,name="serve-unprotected"),) 
