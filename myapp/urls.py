from django.urls import path
from . import views

urlpatterns = [
    path('', views.index ,name="index"),
    path('topics/', views.topics ,name="topic"),
    path('activities/', views.activities ,name="activities"),
    path('login/', views.loginpage ,name="login"),
    path('logout/', views.logoutpage ,name="logout"),
    path('update-user/', views.userupdate ,name="update-user"),
    path('register/', views.registerpage ,name="register"),
    
    path('room/<str:pk>/', views.room, name= "room"),
    path('profile/<str:pk>/', views.userprofile ,name="profile"),
    path('create-room/',views.createroom, name="create-room"),
    path('update-room/<str:pk>/',views.updateroom, name="update-room"),
    path('delete-room/<str:pk>/',views.deleteroom, name="delete-room"),
    path('delete-message/<str:pk>/',views.deletemsg, name="delete-message"),

     
]