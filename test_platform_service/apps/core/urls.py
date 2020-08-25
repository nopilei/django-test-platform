from django.urls import path
from .views import *
urlpatterns = [
    path('', index, name='home'),
    path('tests/create', init_create_test, name='test_create'),
    path('tests/complete', complete_creation, name='test_creation_complete'),
    path('tests/detail/<int:pk>', test_detail, name='test_detail'),
    path('tests/passing/<int:pk>', pass_the_test, name='pass_the_test'),

]