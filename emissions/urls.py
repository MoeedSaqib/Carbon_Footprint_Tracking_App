from django.contrib import admin
from django.urls import path, include
from emissions import views as emissions_views
from .views import register_view
from .views import calculate_emissions
from .views import terminal, log_action
from . import views
from .views import blog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', emissions_views.dashboard, name='dashboard'),
    path('dashboard/', emissions_views.dashboard, name='dashboard'),
    path('accounts/', include('django.contrib.auth.urls')),  
    path('register/', register_view, name='register'),
    path('calculate/', calculate_emissions, name='calculate_emissions'),
    path('calculate/', emissions_views.calculate_emissions, name='calculate_emissions'),  # Path for the emissions calculation
    path('terminal/', emissions_views.terminal, name='terminal'),
    path('terminal/', terminal, name='terminal'),
    path('log-action/', log_action, name='log_action'),
    path('log-eco-action/', views.log_eco_action, name='log_eco_action'),
    path('eco/', emissions_views.eco_page, name='eco_page'),
    path('csr/', views.csr_page, name='csr'),
    path('csr/', emissions_views.csr_page, name='csr_page'),
    path('blog/', views.blog, name='blog'),
     path('blog/', blog, name='blog'),
   
]
