from django.urls import path
from django.conf.urls.static import static
from django.conf import  settings
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgotpassword/', views.forgot_password, name='forgotpassword'),
    path('newpassword/', views.new_password, name='newpassword'),
    path('form/', views.student_form, name='form'),
    path('success/', views.sucess, name='success'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('test/', views.test, name='test'),
]
urlpatterns  += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
