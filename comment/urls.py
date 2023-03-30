# 引入path
from django.urls import path
from comment import views

# 正在部署的应用的名称
app_name = 'comment'

urlpatterns = [
    path('comment_post/<int:ticket_id>/', views.comment_post, name='comment_post')
]