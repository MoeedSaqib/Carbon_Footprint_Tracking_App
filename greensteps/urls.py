
from django.contrib import admin
from django.urls import path , include
from emissions import views as emissions_views  
from django.contrib.auth import views as auth_views
from django.urls import path
from emissions import views as emissions_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', emissions_views.dashboard, name='home'),  # 👈 root path now redirects to dashboard
    path('dashboard/', emissions_views.dashboard, name='dashboard'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('emissions.urls')),
     path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html'
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ), name='password_reset_complete'), 

path('calculate/', emissions_views.calculate_emissions, name='calculate_emissions'),  # Path for the emissions calculation

     path('', include('emissions.urls')), 

     path('eco/', emissions_views.eco_page, name='eco_page'),

path('csr/', emissions_views.csr_page, name='csr_page'),
]

