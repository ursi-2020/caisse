from django.urls import path

from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('products_update/', views.products_update, name='products_update'),
    path('helloworld',views.helloworld,name='helloworld'),
    path('scheduler', views.scheduler, name='scheduler'),
    path('database_update', views.database_update, name='database_update')
]