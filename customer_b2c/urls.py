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
    captcha_image,
    verify_email_change,
    google_map_dashboard,
    start_trip,
    end_trip,
    search_vehicle_vrn,
    search_addresses,
    active_trip,
    end_trip,
    export_trips_excel,
    delete_trip,
    fleet_mileage_dashboard_demo,
    fleet_mileage_dashboard,
    vehicle_mileage_summary,
    vehicle_list,
    mileage_report_pdf,
    driver,
    create_driver_with_licence,
    update_driver_with_licence,
    driver_delete,
    driver_and_licence_logs,
    download_driver_logs,
    user_detail,
    vehicle_logs_view,
    vehicle_logs_api,
    email_logs_api,
    email_logs_view,
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
   
    path("google-map-dashboard", google_map_dashboard, name="google_map_dashboard"),
    
    path("start-trip/", start_trip),
    path("end-trip/<int:trip_id>/", end_trip),
    
    path(
        "search-vehicle-vrn/",
        search_vehicle_vrn,
        name="search_vehicle_vrn"
    ),
    path("search-addresses/", search_addresses),
    path("active-trip/", active_trip, name="active_trip"),
    path("end-trip/", end_trip, name="end_trip"),
    path("trips/export/excel/", export_trips_excel, name="export_trips_excel"),
    path("delete-trip/<int:trip_id>/", delete_trip, name="delete_trip"),
    path("mileage-dashboard-demo/", fleet_mileage_dashboard_demo, name="fleet_mileage_dashboard_demo"),
    path("mileage-dashboard/", fleet_mileage_dashboard, name="fleet_mileage_dashboard"),
    path("api/vehicles/", vehicle_list),
    path("api/mileage/", vehicle_mileage_summary),
    path(
        "mileage-report-pdf/",
        mileage_report_pdf,
        name="mileage_report_pdf"
    ),
    
    
    path("drivers/", driver, name="driver"),
    path("drivers/create/", create_driver_with_licence, name="driver_create"),
    path("driver/<uuid:pk>/update/", update_driver_with_licence, name="driver_update"),
    path('driver/<uuid:driver_id>/delete/', driver_delete, name='driver_delete'),
    path(
        "driver/logs/",
        driver_and_licence_logs,
        name="driver_and_licence_logs"
    ),
    path("driver/logs/download/", download_driver_logs, name="download_driver_logs"),
    path('users/<int:user_id>/', user_detail, name='admin_user_detail'),
    path("vehicle-logs/", vehicle_logs_view, name="vehicle_logs"),
    path("vehicle-logs/api/", vehicle_logs_api, name="vehicle_logs_api"),
    path("reminder-email-logs/", email_logs_view, name="email_logs_view"),
    path("reminder-email-logss/api/", email_logs_api, name="email_logs_api"),







     
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
