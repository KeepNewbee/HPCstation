from django.urls import path
from . import views

app_name = 'document'

urlpatterns = [
    # 
    path('document-list', views.document_list, name='document_list'),

    path('document-detail/<int:id>/', views.document_detail, name='document_detail'),

    path('document-create/', views.document_create, name='document_create'),

    path('document-delete/<int:id>/', views.document_delete, name='document_delete'),

    path('document-update/<int:id>/', views.document_update, name='document_update'),

    path('document-search/', views.document_search, name='document_search'),
]