# 引入path
from django.urls import path
from ticket import views

# 正在部署的应用的名称
app_name = 'ticket'

urlpatterns = [
    path('ticket_list/', views.ticket_list, name='ticket_list'),
    path('ticket_userList/<int:id>', views.ticket_userList,name='ticket_userList'),
    path('ticket_detail/<int:id>/', views.ticket_detail, name='ticket_detail'),
    path('ticket_create/' , views.ticket_create, name='ticket_create'),
    path('ticket_delete/<int:id>/', views.ticket_delete, name='ticket_delete'),
    path('ticket_update/<int:id>/', views.ticket_update, name='ticket_update'),
]