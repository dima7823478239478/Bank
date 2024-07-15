from django.urls import path
from app1.views import index_page
from app1 import views
from django.urls import path
from .converters import OperationIdConverter

urlpatterns = [
    # Другие пути...
    path('', index_page),
    # Пути для банков
    path('banks/', views.BankListView.as_view(), name='bank_list'),
    path('banks/create/', views.create_bank, name='create_bank'),
    path('banks/<str:bank_code>/', views.BankDetailView.as_view(), name='bank_detail'),
    path('banks/<str:bank_code>/edit/', views.edit_bank, name='edit_bank'),
    path('banks/<str:bank_code>/delete/', views.delete_bank, name='delete_bank'),

    # Пути для банкоматов
    path('atms/', views.ATMListView.as_view(), name='atm_list'),
    path('atms/create/', views.create_atm, name='create_atm'),
    path('atms/<str:atm_number>/', views.ATMDetailView.as_view(), name='atm_detail'),
    path('atms/<str:atm_number>/edit/', views.edit_atm, name='edit_atm'),
    path('atms/<str:atm_number>/delete/', views.delete_atm, name='delete_atm'),

    # Пути для клиентов
    path('clients/', views.ClientListView.as_view(), name='client_list'),
    path('clients/create/', views.create_client, name='create_client'),
    path('clients/<str:card_number>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('clients/<str:card_number>/edit/', views.edit_client, name='edit_client'),
    path('clients/<str:card_number>/delete/', views.delete_client, name='delete_client'),

    # Пути для операций
    path('operations/', views.OperationListView.as_view(), name='operation_list'),
    path('operations/create/', views.create_operation, name='create_operation'),
    path('operations/<operation_id:amount>/', views.OperationDetailView.as_view(), name='operation_detail'),
    path('operations/<int:operation_id>/edit/', views.edit_operation, name='edit_operation'),
    path('operations/<int:operation_id>/delete/', views.delete_operation, name='delete_operation'),
]
