from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    index,
    login_view,
    register,
    verify_email,
    logout_view,
    profile,
    request_reset,
    reset_password,
    search_vrn,
    search_mot,
    generate_pdf_endpoint,
    admin_dashboard,
    toggle_block_user,
    delete_users,
    update_user,
    add_vehicle,
    my_vehicle,
    delete_vehicle,
    verify_email_change,
    captcha_image
    
    
    
)

urlpatterns = [
    path('', index, name='index'),

    # Auth
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path(
        'verify-email/<uidb64>/<token>/',
        verify_email,
        name='verify_email'
    ),
    path('logout/', logout_view, name='logout'),

    # Profile
    path('profile/', profile, name='profile'),
    path('profile/<int:user_id>/', profile, name='profile_edit'),
    path('request_reset/', request_reset, name='request_reset'),
    path('reset_password/<uidb64>/<token>/', reset_password, name='reset_password'),
    path('search-vrn/', search_vrn, name='search_vrn'),
    path('search-mot/', search_mot, name='search_mot'),
    path('generate-pdf/', generate_pdf_endpoint, name='generate_pdf'),
    
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('toggle-block/<int:user_id>/', toggle_block_user, name='toggle_block_user'),
    path('delete-users/', delete_users, name='delete_users'),
    path("update-user/", update_user, name="update_user"),
    path('add-vehicle/', add_vehicle, name='add_vehicle'),
    path('my-vehicle/', my_vehicle, name='my_vehicle'),
    path('vehicle/delete/<int:pk>/', delete_vehicle, name='delete_vehicle'),
    path(
    'verify-email-change/<uidb64>/<token>/',verify_email_change,
    name='verify_email_change'
   ),
    path("captcha-image/", captcha_image, name="captcha_image"),

     
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
