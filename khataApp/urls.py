from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('worker/<int:id>/', views.workerPage, name="worker"),
    path('monthWage/', views.monthWages, name='monthWage'),
    path('updateProfile/', views.updateProfile, name='updateProfile'),
    path("updateGiven/", views.updateGiven, name='updateGiven'),
    path('updatePayment/', views.updatePayment, name='updatePayment')
]