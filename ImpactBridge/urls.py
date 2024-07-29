
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
#views for logins and logouts by django
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('donations.urls')),
    path('accounts/',include('allauth.urls')),
    path('profile/', user_views.profile,name='profile'),
   path('donation_post/<int:pk>/kyc/', user_views.kycverify, name='kyc-check'),
   path('Userdefine/',user_views.Userdefine_view,name='Userdefine'),
    path('all_ngos/',user_views.ngo_list, name='all_ngos'),

]
