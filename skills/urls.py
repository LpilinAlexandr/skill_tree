from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.skills, name='skills'),
    path('ajax_form/', views.ajax_form, name='ajax_form'),
    path('download_three/', views.download_three, name='download_three')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)












