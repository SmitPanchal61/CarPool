from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage),
    path('home',views.homepage),
    path('login', views.login),
    path('feedback', views.feedback),
    path('register', views.register),
    path('login_user', views.login_user),
    path("logout_user", views.logout_user),
    # path("user_registration", views.user_registration),
    path("search", views.search),
    path("user_profile", views.user_profile),
    path("update_profile", views.update_profile),
    path("carpools", views.carpools),
    path('<int:carpoolId>',views.fullCarpool),
    path('search/<int:carpoolId>',views.fullCarpoolSearch),
    path('delete/<int:carpoolId>',views.deleteCarpool),
]