
from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('',views.home_view, name='impactbridge-home'),
    path('post_create/',views.donation_post, name='new_donation'),
    path('all_donations/',views.all_donations, name='all_donations'),
    path('paymentstatus/<str:order_id>/', views.payment_status, name='payment_status'),
    path('donation/<int:pk>/',views.donation_detail_view, name='post-detail'),#creating routes based on variables
    path('donate/<int:donation_pk>/<int:user_pk>/', views.donate, name='donate'),
    
    
    
   
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
