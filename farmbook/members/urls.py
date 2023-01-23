from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.sign_up, name='signup'),
    # path('user_login/', views.user_login, name='login'),
    path('user_login/', auth_views.LoginView.as_view(template_name='authenticate/userlogin.html'), name='login'),
    path('user_logout/', auth_views.LogoutView.as_view(template_name='authenticate/userlogout.html'), name='logout'),
    path('user_password_reset/', auth_views.PasswordResetView.as_view(template_name='authenticate/userpassword_reset'
                                                                                    '.html'), name='password_reset'),
    path('user_password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='authenticate'
                                                                                             '/userpassword_reset_done.html'),
         name='password_reset_done'),
    path('user_password_reset_confirm/', auth_views.PasswordResetConfirmView.as_view(template_name='authenticate'
                                                                                                   '/userpassword_reset_confirm.html'),
         name='password_reset_confirm'),
    path('profile/', views.user_profile, name='profile'),
    # path('logout/', views.user_logout, name='logout'),
    path('', include('mogoon.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
