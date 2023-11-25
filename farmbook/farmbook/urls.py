from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

admin.site.site_header = "Developer: Sim KMN"
admin.site.site_title = "Farm Reports"
admin.site.site_index = "Mogoon Farm site"


urlpatterns = [
                  path('admin/clearcache/', include('clearcache.urls')),
                  path('', include('mogoon.urls')),
                  # path('', include('reports.urls')),
                  path('admin/', admin.site.urls),
                  path('members/', include('django.contrib.auth.urls')),
                  path('members/', include('members.urls')),

                  path('api-auth/', include('rest_framework.urls')),

              ] + staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)