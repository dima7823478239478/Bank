from django.urls import path, include
from django.contrib import admin
from app1.views import index_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app1.urls')),
]
