'''定义learning_logs的URL模式'''

from django.urls import path

from . import views


app_name = 'learning_logs'
urlpatterns = [
    # main page
    path('', views.index, name='index')
]