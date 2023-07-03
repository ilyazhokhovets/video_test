from django.urls import path
from . import views

urlpatterns = [
    path('runtest', views.runtest, name='download'),
path('', views.home, name='home'),

]