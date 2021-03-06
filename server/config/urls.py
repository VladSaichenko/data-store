from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.tables.urls')),
    path('users/', include('apps.users.urls')),
    path('report/', include('apps.reports.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    import debug_toolbar

    urlpatterns += [
          path('__debug__/', include(debug_toolbar.urls)),
    ]
