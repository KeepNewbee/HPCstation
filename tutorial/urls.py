from django.urls import path

from . import views

app_name = 'tutorial'
urlpatterns = [
    path('tutorial-detail/<int:id>/', views.tutorial_detail, name='tutorial_detail'),
    # path('posts/<int:pk>/', views.detail, name='detail'),

]