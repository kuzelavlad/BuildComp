from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from houses import settings

urlpatterns = [
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('admin/', admin.site.urls),
    path('', include('housestroy.urls')),
    path('', include('contacts.urls')),
    path('', include('blog.urls')),
    path('', include('application.urls')),
    path('', include('personal.urls')),
    # path('', include('revenge.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
