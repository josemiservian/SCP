"""scp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
# Django
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


#el namespace se utilziara para referenciar templates en otros 
urlpatterns = [
    path('admin/', admin.site.urls),
 
 
    #path('', include('apps.cuentas.urls')),
    path('administracion/', include(('apps.administracion.urls', 'administracion'), namespace='administracion')),
    path('gestion/', include(('apps.gestion.urls', 'gestion'), namespace='gestion')),
    path('proyectos/', include(('apps.proyectos.urls', 'proyectos'), namespace='proyectos')),
    path('reportes/', include(('apps.reportes.urls', 'reportes'), namespace='reportes')),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)