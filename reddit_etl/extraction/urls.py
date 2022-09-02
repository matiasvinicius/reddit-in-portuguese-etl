from django.urls import include, path
from extraction import views

urlpatterns = [
    path('status', views.status, name='status'),
]