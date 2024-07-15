from django.urls import path, register_converter
from . import views

class OperationIdConverter:
    regex = '[\d\.]+'

    def to_python(self, value):
        try:
            return float(value)
        except ValueError:
            raise ValueError('Invalid operation ID')

    def to_url(self, value):
        return str(value)

register_converter(OperationIdConverter, 'operation_id')

urlpatterns = [
    path('operations/<operation_id:amount>/', views.OperationDetailView.as_view(), name='operation_detail'),
]
