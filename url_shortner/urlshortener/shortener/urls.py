from django.urls import path
from . import views

urlpatterns = [
    path('shorten/', views.shorten_url, name='shorten'),
    path('expand/<str:code>/', views.expand_url, name='expand'),
]
