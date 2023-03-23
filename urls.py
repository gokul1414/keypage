from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
urlpatterns = [
    path('',views.welcome_page,name='welcome'),
    path('home/',views.home,name='home'),
    path('about/',views.page_about,name='about'),
    path('homeabout/',views.base_about,name='baseabout'),
    path('newpost/',views.newpost,name='create_post'),
    path('login/',views.user_login,name='login'),
    path('register/',views.user_register,name='register'),
    path('logout/',views.user_logout,name='logout'),

    
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)