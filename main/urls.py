from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sira/', views.sira, name='sira'),
    path('riyad_useimin/', views.riyad_useimin, name='riyad_useimin'),
    path('tafsir/', views.tafsir, name='tafsir'),
    path('admin-info/', views.admin_info, name='admin_info'),
    path('api/latest-video/', views.latest_video, name='latest_video'),
    path('api/cron/parse-youtube/', views.cron_parse_youtube, name='cron_parse_youtube'),
]