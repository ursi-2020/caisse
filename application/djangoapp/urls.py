from django.urls import path

from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('products_update/', views.products_update, name='products_update'),
    path('helloworld',views.helloworld,name='helloworld'),
    path('scheduler/', views.scheduler, name='scheduler'),
    path('database_update_scheduled', views.database_update_scheduled, name='database_update_scheduled'),
    path('database/', views.database, name='database'),
    path('tickets/', views.tickets, name='tickets'),

    path('sales_simulation', views.sales_simulation, name='Sales Simulation'),

    path('api/tickets/', views.get_tickets, name='Get Tickets'),
    path('api/new_tickets/', views.get_new_tickets, name='Get New Tickets')

]