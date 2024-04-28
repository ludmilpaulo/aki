from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('shops/', include('shop.urls')), 
    path('accounts/', include('account.urls')), 
    path('orders/', include('order.urls')),
    path('info/', include('information.urls')),
    path('report/', include('report.urls')),
    path('careers/', include('careers.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    path('admin/', admin.site.urls),

]


if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
