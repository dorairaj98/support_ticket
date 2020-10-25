from django.contrib import admin
from django.urls import path, include
from ticket import views as user_view
from django.contrib.auth import views as auth

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('ticket.urls')),
    path('login/', user_view.Login, name='login'),
    path('logout/', auth.LogoutView.as_view(template_name='ticket/login.html'), name='logout'),
    path('dashboard/', user_view.dashboard, name='dashboard'),
    path('submit_form/', user_view.submit_ticket, name='submit_form'),
]